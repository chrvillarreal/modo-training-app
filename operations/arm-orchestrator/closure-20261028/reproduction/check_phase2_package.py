import pathlib,json,hashlib,subprocess,sys
root=pathlib.Path('/workspace/work/phase2-arm/operations/arm-orchestrator')
session=pathlib.Path('/workspace/work/phase2')
sys.path.insert(0,str(root));from arm import Orchestrator
o=Orchestrator(session/'arm-session.sqlite',read_only=True)
assert o.verify()
files=[p for p in root.rglob('*') if p.is_file() and '__pycache__' not in str(p)]
sources=files+[p for p in session.rglob('*') if p.is_file()]+[p for p in pathlib.Path('/workspace/work/arm-continuation-20261028').rglob('*') if p.is_file()]
missing=[]
for run in o.export()['runs']:
 if not run['evidence']:continue
 e=json.loads(run['evidence'])
 if not any(p.name==e['file'] and hashlib.sha256(p.read_bytes()).hexdigest()==e['sha256'] for p in sources):missing.append(e)
assert not missing,missing
for p,h in json.loads((root/'MANIFEST.json').read_text()).items():assert hashlib.sha256((root/p).read_bytes()).hexdigest()==h,p
base='c86bdfc133a1191d446a84984d758e50975f75fe'
repo=root.parents[1]
for name in ['arm.sqlite','snapshot.json','INFORME.md']:
 assert (root/name).read_bytes()==subprocess.check_output(['git','-C',str(repo),'show',base+':operations/arm-orchestrator/'+name])
subprocess.run(['git','-C',str(repo),'diff','--check'],check=True)
paths=subprocess.check_output(['git','-C',str(repo),'diff','--name-only','HEAD'],text=True).splitlines()+subprocess.check_output(['git','-C',str(repo),'ls-files','--others','--exclude-standard'],text=True).splitlines()
assert all(p.startswith('operations/arm-orchestrator/') for p in paths)
running=o.db.execute("SELECT title FROM tasks WHERE status='running'").fetchall()
assert all(r['title']=='Verificar integridad del paquete de cierre y alcance local' for r in running),[dict(r) for r in running]
for p in (root/'proposals/phase2-20261028').glob('*.yml'):
 data=json.loads(p.read_text());assert data['permissions']=={'contents':'read'};assert 'pull_request' in data['on']
print(json.dumps({'event_chain_valid':True,'all_run_evidence_resolves':True,'historical_files_preserved':True,'changes_confined_to_arm_package':True,'manifest_entries':len(json.loads((root/'MANIFEST.json').read_text())),'pending_B':o.db.execute("SELECT count(*) FROM tasks WHERE title LIKE 'Pendiente B-%' AND status='awaiting_approval'").fetchone()[0]},indent=2))
