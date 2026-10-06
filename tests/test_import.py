import subprocess
import sys
import unittest


class PackageImportTest(unittest.TestCase):

    def test_import_without_pkg_resources(self):
        if sys.version_info < (3, 8):
            self.skipTest('importlib.metadata is unavailable')

        subprocess.check_call([
            sys.executable,
            '-c',
            "import sys; sys.modules['pkg_resources'] = None; "
            "import pyuri; assert pyuri.URI; assert pyuri.__version__"
        ])
