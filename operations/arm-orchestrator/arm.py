"""ARM Orchestrator 1.0: local evidence ledger and supervised task router.
No remote writes, shell execution, API keys or autonomous paid model calls.
"""
import argparse, hashlib, json, sqlite3, time, uuid
from pathlib import Path

PROJECTS = ('rm-training', 'modo-training-app', 'calculadora-nutricion-deportiva')
SAFE = {'audit': 'development', 'test': 'ux-qa', 'review': 'ux-qa', 'draft_patch': 'development'}
SENSITIVE = {'push_branch', 'create_pr', 'preview_deploy'}
FORBIDDEN = {'write_main', 'merge_pr', 'production_deploy', 'production_db', 'spend', 'send_message'}

def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':'))

def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()

class Orchestrator:
    def __init__(self, path='arm.sqlite'):
        self.db = sqlite3.connect(path)
        self.db.row_factory = sqlite3.Row
        self.db.execute('PRAGMA foreign_keys=ON')
        self.db.executescript('''
        CREATE TABLE IF NOT EXISTS projects (id TEXT PRIMARY KEY, repo TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS tasks (id TEXT PRIMARY KEY, project TEXT REFERENCES projects(id), title TEXT NOT NULL, priority TEXT CHECK(priority IN ('P0','P1','P2')), action TEXT NOT NULL, branch TEXT NOT NULL, sha TEXT NOT NULL, status TEXT NOT NULL, agent TEXT NOT NULL, payload TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS runs (id TEXT PRIMARY KEY, task TEXT REFERENCES tasks(id), status TEXT NOT NULL, started REAL NOT NULL, finished REAL, evidence TEXT);
        CREATE TABLE IF NOT EXISTS approvals (id TEXT PRIMARY KEY, task TEXT REFERENCES tasks(id), fingerprint TEXT NOT NULL, status TEXT NOT NULL, expires REAL NOT NULL, decision_reference TEXT);
        CREATE TABLE IF NOT EXISTS events (seq INTEGER PRIMARY KEY, at REAL NOT NULL, kind TEXT NOT NULL, data TEXT NOT NULL, previous TEXT NOT NULL, hash TEXT NOT NULL);
        ''')
        with self.db:
            for p in PROJECTS:
                self.db.execute('INSERT OR IGNORE INTO projects VALUES (?,?)', (p, 'chrvillarreal/'+p))

    def event(self, kind, data):
        previous = self.db.execute('SELECT hash FROM events ORDER BY seq DESC LIMIT 1').fetchone()
        prev = previous[0] if previous else '0'*64
        at = time.time()
        self.db.execute('INSERT INTO events(at,kind,data,previous,hash) VALUES(?,?,?,?,?)', (at,kind,canonical(data),prev,digest([at,kind,data,prev])))

    def task(self, project, title, priority, action, branch, sha, payload=None):
        if action not in set(SAFE) | SENSITIVE | FORBIDDEN: raise ValueError('Unknown action: denied')
        if not title.strip() or not branch.strip(): raise ValueError('Title/branch required')
        if len(sha)!=40 or any(c not in '0123456789abcdef' for c in sha): raise ValueError('Pin a commit SHA')
        ident = str(uuid.uuid4())
        status = 'blocked' if action in FORBIDDEN or (action in SENSITIVE and branch in ('main','master')) else 'awaiting_approval' if action in SENSITIVE else 'queued'
        with self.db:
            self.db.execute('INSERT INTO tasks VALUES(?,?,?,?,?,?,?,?,?,?)',(ident,project,title,priority,action,branch,sha,status,SAFE.get(action,'human'),canonical(payload or {})))
            self.event('task.created', {'id':ident,'status':status})
        return ident

    def get(self, task):
        row=self.db.execute('SELECT * FROM tasks WHERE id=?',(task,)).fetchone()
        if row is None: raise ValueError('Unknown task')
        return dict(row)

    def request_approval(self, task, ttl=86400):
        t=self.get(task)
        if t['status']!='awaiting_approval' or not 0<ttl<=86400: raise ValueError('Not approvable')
        ident=str(uuid.uuid4())
        with self.db:
            self.db.execute('INSERT INTO approvals VALUES(?,?,?,?,?,NULL)',(ident,task,digest(t),'pending',time.time()+ttl))
            self.event('approval.requested',{'id':ident,'task':task})
        return ident

    def decide(self, approval, approve, decision_reference):
        # Records a human decision; never grants a remote executor credentials.
        if not decision_reference.strip(): raise ValueError('Explicit human decision reference required')
        row=self.db.execute('SELECT * FROM approvals WHERE id=?',(approval,)).fetchone()
        if not row or row['status']!='pending' or row['expires']<=time.time(): raise ValueError('Invalid/expired approval')
        if digest(self.get(row['task']))!=row['fingerprint']: raise ValueError('Scope changed')
        with self.db:
            self.db.execute('UPDATE approvals SET status=?,decision_reference=? WHERE id=?',('recorded_approved' if approve else 'rejected',decision_reference,approval))
            self.event('approval.decision',{'id':approval,'approved':approve,'reference':decision_reference})
        # Sensitive tasks stay awaiting_approval: connector-side approval still required.

    def start(self, task):
        t=self.get(task)
        if t['action'] not in SAFE or t['status']!='queued': raise ValueError('No authorized safe task available')
        ident=str(uuid.uuid4())
        with self.db:
            changed=self.db.execute("UPDATE tasks SET status='running' WHERE id=? AND status='queued'",(task,)).rowcount
            if changed!=1: raise ValueError('Already claimed')
            self.db.execute('INSERT INTO runs VALUES(?,?,?,?,NULL,NULL)',(ident,task,'running',time.time()))
            self.event('run.started',{'id':ident,'task':task})
        return ident

    def finish(self, run, status, evidence):
        if status not in ('passed','failed','blocked'): raise ValueError('Unknown result')
        p=Path(evidence)
        if not p.is_file() or p.stat().st_size==0: raise ValueError('Nonempty evidence file required')
        row=self.db.execute('SELECT * FROM runs WHERE id=?',(run,)).fetchone()
        if not row or row['status']!='running': raise ValueError('Run is not active')
        item={'file':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
        with self.db:
            self.db.execute('UPDATE runs SET status=?,finished=?,evidence=? WHERE id=?',(status,time.time(),canonical(item),run))
            self.db.execute('UPDATE tasks SET status=? WHERE id=?',('done' if status=='passed' else status,row['task']))
            self.event('run.finished',{'id':run,'status':status,'evidence':item})

    def verify(self):
        prev='0'*64
        for r in self.db.execute('SELECT * FROM events ORDER BY seq'):
            if r['previous']!=prev or r['hash']!=digest([r['at'],r['kind'],json.loads(r['data']),prev]): return False
            prev=r['hash']
        return True

    def export(self):
        return {t:[dict(r) for r in self.db.execute('SELECT * FROM '+t)] for t in ('projects','tasks','runs','approvals','events')}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--db',default='arm.sqlite')
    sub=p.add_subparsers(dest='cmd',required=True)
    sub.add_parser('status'); sub.add_parser('verify')
    add=sub.add_parser('task')
    for name in ('project','title','priority','action','branch','sha'): add.add_argument('--'+name,required=True)
    start=sub.add_parser('start');start.add_argument('task')
    finish=sub.add_parser('finish');finish.add_argument('run');finish.add_argument('status',choices=['passed','failed','blocked']);finish.add_argument('evidence')
    approval=sub.add_parser('request-approval');approval.add_argument('task')
    args=vars(p.parse_args());db=args.pop('db');cmd=args.pop('cmd');o=Orchestrator(db)
    if cmd=='status': result=o.export()
    elif cmd=='verify': result={'valid':o.verify()}
    elif cmd=='task': result={'task':o.task(**args)}
    elif cmd=='start':result={'run':o.start(**args)}
    elif cmd=='finish':result=o.finish(**args)
    else:result={'approval':o.request_approval(**args)}
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
