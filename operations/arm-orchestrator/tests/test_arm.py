import unittest, tempfile, pathlib, sqlite3, sys
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from arm import Orchestrator, PROJECTS, FORBIDDEN
class Tests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.o=Orchestrator(pathlib.Path(self.tmp.name)/'db');self.e=pathlib.Path(self.tmp.name)/'proof.log';self.e.write_text('Observed test output')
 def tearDown(self): self.o.db.close();self.tmp.cleanup()
 def task(self,action='test',branch='audit/local',sha='a'*40):return self.o.task(PROJECTS[0],'Audit','P1',action,branch,sha)
 def test_registry(self):self.assertEqual(len(self.o.export()['projects']),3)
 def test_unknown_project(self):
  with self.assertRaises(sqlite3.IntegrityError):self.o.task('other','X','P1','test','audit','a'*40)
 def test_unknown_action(self):
  with self.assertRaises(ValueError):self.task('shell')
 def test_sha_required(self):
  with self.assertRaises(ValueError):self.task(sha='main')
 def test_priority(self):
  with self.assertRaises(sqlite3.IntegrityError):self.o.task(PROJECTS[0],'X','urgent','test','audit','a'*40)
 def test_safe_run(self):
  t=self.task();r=self.o.start(t);self.o.finish(r,'passed',self.e);self.assertEqual(self.o.get(t)['status'],'done');self.assertTrue(self.o.verify())
 def test_failure_not_done(self):
  t=self.task();self.o.finish(self.o.start(t),'failed',self.e);self.assertEqual(self.o.get(t)['status'],'failed')
 def test_block_not_pass(self):
  t=self.task();self.o.finish(self.o.start(t),'blocked',self.e);self.assertEqual(self.o.get(t)['status'],'blocked')
 def test_evidence_required(self):
  r=self.o.start(self.task())
  with self.assertRaises(ValueError):self.o.finish(r,'passed','missing.log')
 def test_duplicate_start(self):
  t=self.task();self.o.start(t)
  with self.assertRaises(ValueError):self.o.start(t)
 def test_duplicate_finish(self):
  r=self.o.start(self.task());self.o.finish(r,'passed',self.e)
  with self.assertRaises(ValueError):self.o.finish(r,'passed',self.e)
 def test_forbidden(self):
  for action in FORBIDDEN:
   t=self.task(action)
   with self.assertRaises(ValueError):self.o.start(t)
   with self.assertRaises(ValueError):self.o.request_approval(t)
 def test_main_write_block(self):self.assertEqual(self.o.get(self.task('push_branch','main'))['status'],'blocked')
 def test_sensitive_no_executor(self):
  t=self.task('push_branch');a=self.o.request_approval(t);self.o.decide(a,True,'TEST ONLY user instruction')
  with self.assertRaises(ValueError):self.o.start(t)
 def test_approval_reuse(self):
  a=self.o.request_approval(self.task('create_pr'));self.o.decide(a,False,'TEST refusal')
  with self.assertRaises(ValueError):self.o.decide(a,True,'TEST reversal')
 def test_approval_expiry(self):
  a=self.o.request_approval(self.task('create_pr'));self.o.db.execute('UPDATE approvals SET expires=0 WHERE id=?',(a,));self.o.db.commit()
  with self.assertRaises(ValueError):self.o.decide(a,True,'TEST')
 def test_approval_scope(self):
  t=self.task('create_pr');a=self.o.request_approval(t);self.o.db.execute('UPDATE tasks SET sha=? WHERE id=?',('b'*40,t));self.o.db.commit()
  with self.assertRaises(ValueError):self.o.decide(a,True,'TEST')
 def test_no_self_approval(self):
  a=self.o.request_approval(self.task('create_pr'))
  with self.assertRaises(ValueError):self.o.decide(a,True,'')
 def test_tampering(self):
  self.task();self.o.db.execute("UPDATE events SET kind='changed'");self.assertFalse(self.o.verify())
 def test_persistence(self):
  self.task();second=Orchestrator(pathlib.Path(self.tmp.name)/'db');self.assertEqual(len(second.export()['tasks']),1);second.db.close()
if __name__=='__main__':unittest.main()
