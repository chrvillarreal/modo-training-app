"""CLI acceptance using temporary ledgers and synthetic evidence only."""
import hashlib
import json
import pathlib
import sqlite3
import subprocess
import sys
import tempfile
import unittest

from arm import Orchestrator


class CliWorkflow(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.tmp.name)
        self.db = self.root / 'ledger.sqlite'
        self.script = pathlib.Path(__file__).resolve().parents[1] / 'arm.py'

    def tearDown(self):
        self.tmp.cleanup()

    def cli(self, *args):
        return subprocess.run(
            [sys.executable, str(self.script), '--db', str(self.db), *args],
            capture_output=True, text=True, timeout=10)

    def seed(self):
        o = Orchestrator(self.db)
        o.task('modo-training-app', 'Synthetic review', 'P2', 'audit',
               'audit/test', 'a' * 40)
        o.db.close()

    def test_verify_missing_ledger_fails_without_creating_it(self):
        result = self.cli('verify')
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.db.exists())
        self.assertFalse(json.loads(result.stdout)['valid'])

    def test_verify_empty_file_fails_without_initializing_it(self):
        self.db.write_bytes(b'')
        result = self.cli('verify')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.db.read_bytes(), b'')
        self.assertFalse(json.loads(result.stdout)['valid'])

    def test_verify_malformed_event_json_reports_invalid(self):
        self.seed()
        with sqlite3.connect(self.db) as connection:
            connection.execute("UPDATE events SET data='not-json'")
        result = self.cli('verify')
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(json.loads(result.stdout)['valid'])
        self.assertNotIn('Traceback', result.stderr)

    def test_verify_non_sqlite_file_reports_invalid_without_changes(self):
        self.db.write_bytes(b'Synthetic non-SQLite content')
        result = self.cli('verify')
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(json.loads(result.stdout)['valid'])
        self.assertEqual(self.db.read_bytes(), b'Synthetic non-SQLite content')

    def test_verify_wrong_sqlite_schema_is_invalid(self):
        with sqlite3.connect(self.db) as connection:
            connection.execute('CREATE TABLE events (seq INTEGER)')
        before = self.db.read_bytes()
        result = self.cli('verify')
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(json.loads(result.stdout)['valid'])
        self.assertEqual(self.db.read_bytes(), before)

    def test_complete_supervised_cli_lifecycle(self):
        result = self.cli('task', '--project', 'modo-training-app', '--title',
                          'Synthetic patch acceptance', '--priority', 'P2',
                          '--action', 'draft_patch', '--branch', 'audit/test',
                          '--sha', 'a' * 40)
        self.assertEqual(result.returncode, 0, result.stderr)
        task = json.loads(result.stdout)['task']
        started = self.cli('start', task)
        self.assertEqual(started.returncode, 0, started.stderr)
        run = json.loads(started.stdout)['run']
        evidence = self.root / 'proof.log'
        evidence.write_text('Synthetic QA observed: passed\n')
        finished = self.cli('finish', run, 'passed', str(evidence))
        self.assertEqual(finished.returncode, 0, finished.stderr)
        exported = self.cli('status')
        self.assertEqual(exported.returncode, 0, exported.stderr)
        state = json.loads(exported.stdout)
        self.assertEqual(state['tasks'][0]['status'], 'done')
        self.assertEqual(state['tasks'][0]['agent'], 'development')
        self.assertEqual(state['runs'][0]['status'], 'passed')
        self.assertEqual(json.loads(state['runs'][0]['evidence'])['sha256'],
                         hashlib.sha256(evidence.read_bytes()).hexdigest())
        before = hashlib.sha256(self.db.read_bytes()).hexdigest()
        verified = self.cli('verify')
        self.assertEqual(verified.returncode, 0, verified.stderr)
        self.assertTrue(json.loads(verified.stdout)['valid'])
        self.assertEqual(hashlib.sha256(self.db.read_bytes()).hexdigest(), before)
        self.assertNotEqual(self.cli('finish', run, 'passed', str(evidence)).returncode, 0)
