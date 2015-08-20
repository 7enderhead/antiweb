import unittest
from unittest.mock import patch
from antiweb import main
import sys
import os
import tempfile
import shutil
import errno

class Test_Antiweb(unittest.TestCase):


    def setUp(self):

        self.test_dir = tempfile.mkdtemp()
        self.testfile_source = "#@start()\n\n#@include(test_area)\n\n#@start(test_area)\n#This is test_area text\n#@(test_area)"
        with open(os.path.join(self.test_dir, "testfile.py"), "w") as test:
            test.write(self.testfile_source)

    def test_antiweb(self):
        self.test_args = ['antiweb.py', '-i', "-o docs", os.path.join(self.test_dir, "testfile.py")]
        with patch.object(sys, 'argv', self.test_args):
            success = main()
        self.assertTrue(success)

    def tearDown(self):

        shutil.rmtree(self.test_dir)
        



if __name__ == '__main__':
    unittest.main()