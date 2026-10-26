import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from validate_catalog import validate

class PortalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = json.loads((ROOT/'data/catalog.json').read_text(encoding='utf-8'))

    def test_stock_catalog(self):
        self.assertEqual(1, len(validate(self.catalog)['products']))

    def test_duplicate_id_rejected(self):
        p = copy.deepcopy(self.catalog)
        p['products'].append(copy.deepcopy(p['products'][0]))
        with self.assertRaises(ValueError): validate(p)

    def test_unknown_field_rejected(self):
        p = copy.deepcopy(self.catalog)
        p['products'][0]['private_notes'] = 'internal'
        with self.assertRaises(ValueError): validate(p)

    def test_path_traversal_rejected(self):
        p = copy.deepcopy(self.catalog)
        p['products'][0]['launch_path']='/tools/../secret/'
        with self.assertRaises(ValueError): validate(p)

    def test_missing_internal_tool_rejected(self):
        p=copy.deepcopy(self.catalog)
        p['products'][0]['launch_path']='/tools/missing/'
        with self.assertRaises(ValueError): validate(p)

    def test_local_link_rejected(self):
        p=copy.deepcopy(self.catalog)
        p['products'][0]['links']=[{'type':'website','url':'https://localhost/private','label':'oops'}]
        with self.assertRaises(ValueError): validate(p)

    def test_non_https_link_rejected(self):
        p=copy.deepcopy(self.catalog)
        p['products'][0]['links']=[{'type':'website','url':'http://example.org','label':'oops'}]
        with self.assertRaises(ValueError): validate(p)

    def test_secret_in_summary_rejected(self):
        p=copy.deepcopy(self.catalog)
        p['products'][0]['summary']='foo C:\\Users\\me\\internal'
        with self.assertRaises(ValueError): validate(p)

    def test_offline_tool_present(self):
        self.assertTrue((ROOT/'tools/json/tool.js').is_file())
        content=(ROOT/'tools/json/tool.js').read_text(encoding='utf-8')
        self.assertIn('JSON.parse', content)
        self.assertNotIn('fetch(', content)

if __name__=='__main__': unittest.main()
