import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class ScriptVersionTest(unittest.TestCase):
    def test_local_script_references_match_content(self):
        module = (ROOT / 'Module.sgmodule').read_text('utf-8')
        urls = re.findall(r'https://raw\.githubusercontent\.com/miketoryan/Shadowrocket-Fusion-Personal/main/scripts/([\w.-]+\.js)(?:\?v=([^,\s]+))?', module)
        self.assertTrue(urls)
        for name, version in urls:
            digest = hashlib.sha256((ROOT / 'scripts' / name).read_text('utf-8').rstrip().encode('utf-8')).hexdigest()[:16]
            self.assertEqual(version, digest, f'{name}: update the script URL version when the script changes')

if __name__ == '__main__':
    unittest.main()
