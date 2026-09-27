import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location('corrections', Path(__file__).resolve().parents[1] / 'scripts/corrections.py')
c = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(c)

class CorrectionsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'company'
        (self.root / 'wiki').mkdir(parents=True)
        self.page = self.root / 'wiki/p.md'
        self.original = b'old\r\nUntouched \xc3\xa9\r\n'
        self.page.write_bytes(self.original)

    def record(self, rewrite='new'):
        return c.record_correction(self.root, dict(original='old', rewrite=rewrite, reason='style', scope='p.md', example='old -> new'))

    def propose(self):
        self.record(); self.record()
        return c.propose_rule(self.root, 'p.md', 'style')

    def accept(self, pid):
        c.accept_rule(self.root, pid, 'founder', hashlib.sha256(self.page.read_bytes()).hexdigest())

    def test_repeated_reason_and_regression(self):
        for count in (0, 1):
            with self.assertRaises(ValueError): c.propose_rule(self.root, 'p.md', 'style')
            self.record()
        pid = c.propose_rule(self.root, 'p.md', 'style')
        self.accept(pid)
        self.assertTrue(self.page.read_bytes().startswith(self.original))
        self.assertEqual(c.apply_corrections(self.root, 'p.md', 'old\r\nkeep'), 'new\r\nkeep')
        self.assertEqual(c.apply_corrections(self.root, 'other.md', 'old'), 'old')
        for file in (self.root/'wiki/corrections').glob('*.json'):
            file.write_text('{}')
        self.assertEqual(c.apply_corrections(self.root, 'p.md', 'old'), 'new')

    def test_stale_digest_and_conflict(self):
        pid = self.propose()
        with self.assertRaises(ValueError): c.accept_rule(self.root, pid, 'founder', '0'*64)
        self.assertEqual(self.page.read_bytes(), self.original)
        self.record('contradiction')
        conflict = c.propose_rule(self.root, 'p.md', 'style')
        with self.assertRaises(ValueError): self.accept(conflict)
        self.assertEqual(c.apply_corrections(self.root, 'p.md', 'old'), 'old')

    def test_accept_failure_rolls_back_page_and_pending(self):
        pid = self.propose()
        with patch.object(c, '_save_proposals', side_effect=OSError('disk')):
            with self.assertRaises(OSError): self.accept(pid)
        self.assertEqual(self.page.read_bytes(), self.original)
        self.assertEqual(c.apply_corrections(self.root, 'p.md', 'old'), 'old')
        self.accept(pid)
        with self.assertRaises(ValueError): self.accept(pid)

    def test_page_write_failure_keeps_pending(self):
        pid = self.propose()
        with patch.object(c, '_atomic_write', side_effect=OSError('disk')):
            with self.assertRaises(OSError): self.accept(pid)
        self.assertEqual(c.apply_corrections(self.root, 'p.md', 'old'), 'old')

    def test_symlink_boundaries(self):
        outside = Path(self.tmp.name)/'outside'
        outside.mkdir()
        for relative in ('wiki', 'wiki/corrections', 'wiki/proposals.json', 'wiki/p.md'):
            with self.subTest(relative=relative):
                path = self.root/relative
                if path.exists(): path.rename(path.with_name(path.name+'.saved'))
                path.symlink_to(outside, target_is_directory=True)
                try:
                    operation = lambda: c.propose_rule(self.root, 'p.md', 'style')
                    with self.assertRaises(ValueError): operation()
                finally:
                    path.unlink()
                    saved = path.with_name(path.name+'.saved')
                    if saved.exists(): saved.rename(path)
        alias = Path(self.tmp.name)/'alias'
        alias.symlink_to(self.root, target_is_directory=True)
        with self.assertRaises(ValueError): c.apply_corrections(alias, 'p.md', 'old')

    def test_temp_symlink_not_followed(self):
        victim = Path(self.tmp.name)/'victim'
        victim.write_bytes(b'safe')
        (self.root/'wiki/proposals.json.new').symlink_to(victim)
        self.propose()
        self.assertEqual(victim.read_bytes(), b'safe')

    def test_typed_data_and_paths(self):
        for scope in ('../escape', '/abs', '.', ''):
            with self.assertRaises(ValueError): c.apply_corrections(self.root, scope, 'old')
        for value in (None, [], {'original': 3, 'rewrite':'x','reason':'r','scope':'p.md'}):
            with self.assertRaises(ValueError): c.record_correction(self.root, value)
        (self.root/'wiki/proposals.json').write_text('{}')
        with self.assertRaises(ValueError): c.apply_corrections(self.root, 'p.md', 'old')

    def test_symlink_evidence_read_rejected(self):
        self.propose()
        file = next((self.root/'wiki/corrections').glob('*.json'))
        content = file.read_bytes()
        external = Path(self.tmp.name)/'external.json'; external.write_bytes(content)
        file.unlink(); file.symlink_to(external)
        with self.assertRaises(ValueError): c.propose_rule(self.root, 'p.md', 'style')

    def test_existing_accepted_conflict_rejected(self):
        pid=self.propose(); self.accept(pid)
        for _ in range(2):
            c.record_correction(self.root, dict(original='old',rewrite='other',reason='different',scope='p.md'))
        pid=c.propose_rule(self.root,'p.md','different')
        with self.assertRaises(ValueError): self.accept(pid)
        self.assertEqual(c.apply_corrections(self.root,'p.md','old'),'new')

    def test_noncanonical_reserved_scopes_and_missing_root(self):
        for scope in ('./p.md', 'pages//p.md', 'proposals.json', 'corrections/rule.md'):
            with self.assertRaises(ValueError): c.apply_corrections(self.root,scope,'old')
        with self.assertRaises(ValueError): c.apply_corrections(self.root/'missing','p.md','old')

    def test_conflicting_accepted_store_is_explicit(self):
        pid=self.propose(); self.accept(pid)
        path=self.root/'wiki/proposals.json'
        store=json.loads(path.read_text())
        other=dict(store[0],id='another',rewrites=[{'original':'old','rewrite':'conflict'}])
        path.write_text(json.dumps(store+[other]))
        with self.assertRaisesRegex(ValueError,'conflict'): c.apply_corrections(self.root,'p.md','old')
