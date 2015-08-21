#@start()
#@cstart(imports)

import unittest
from unittest.mock import patch
from antiweb import main
import sys
import os
import tempfile
import shutil
import errno

#@(imports)

#@start(Test_Antiweb)
#********************
#Unittest for antiweb
#********************
"""
This python file runs a unittest on antiweb to test all possible combinations for accuracy and correctness
"""

#@include(preparation)
#@include(testcase)
#@(Test_Antiweb)

class Test_Antiweb(unittest.TestCase):

    #@start(preparation)
    #This function will be called before each Test. It copies the file to process into the temp directory of the test
    #@code
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.origin_path = os.path.join(os.getcwd(), os.path.join("unittest", "small_testfile.py"))
        self.destination_path = os.path.join(self.test_dir, "small_testfile.py")

        shutil.copyfile(self.origin_path, self.destination_path)
    #@edoc
    
    #The :py:class:`functional(self, directory, filename, compare_path, assert_input)` class tests if antiweb was fully executed and if the files were created in the correct a
    #@code
    def functional(self, directory, filename, compare_path, assert_input):

        self.assertTrue(assert_input)

        self.compare(directory, filename, compare_path)
    #@edoc
    
    #In some cases the index.rst file should not be created, the :py:class:`file_not_exist(self, path)` class will verify that expectation
    #@code
    def file_not_exist(self, path):

        self.assertFalse(os.path.isfile(path))

    def compare(self, directory, filename, compare_path):

        with open(os.path.join(self.test_dir, directory, filename)) as output:
            antiweb_output = output.readlines()
        with open(compare_path) as compare:
            antiweb_compare = compare.readlines()
        self.assertEqual(antiweb_output, antiweb_compare)
    #@edoc
    #@(preparation)
    
    #@start(testcase)
    #This is one of eight tests that will be performed. ``compare_path_small_testfile`` is the path to the file to compare the output with.
    #``compare_path_index`` is the counterpart for the created index.rst file
    #The arguments which would normally be set in the command prompt are set using ``patch.object` wich is imported from :py:class:`unittest.mock` 
    #After the arguments are set :py:class:``self.functional`` is called to compare the expectation with the actual output.
    
    #@code
    
    def test_antiweb_i_o(self):
        compare_path_small_testfile = os.path.join("unittest","small_testfile.rst")
        compare_path_index = os.path.join("unittest","index_o.rst")
        self.test_args = ['antiweb.py', '-i', "-o"+"docs", os.path.join(self.test_dir, "small_testfile.py")]

        with patch.object(sys, 'argv', self.test_args):
            self.functional("", "docs.rst", compare_path_small_testfile, main())
            self.functional("", "index.rst", compare_path_index, os.path.isfile(os.path.join(self.test_dir, "index.rst")))
    
    #@edoc
    #@(preparation)

    def test_antiweb_o(self):
        compare_path_small_testfile = os.path.join("unittest","small_testfile.rst")
        self.test_args = ['antiweb.py', "-o"+"docs", os.path.join(self.test_dir, "small_testfile.py")]

        with patch.object(sys, 'argv', self.test_args):
            self.functional("", "docs.rst", compare_path_small_testfile, main())
            self.file_not_exist(os.path.join(self.test_dir, "index.rst"))


    def test_antiweb_i(self):
        compare_path_small_testfile = os.path.join("unittest","small_testfile.rst")
        compare_path_index = os.path.join("unittest","index.rst")
        self.test_args = ['antiweb.py', '-i', os.path.join(self.test_dir, "small_testfile.py")]

        with patch.object(sys, 'argv', self.test_args):

            self.functional("", "small_testfile.rst", compare_path_small_testfile, main())
            self.functional("", "index.rst", compare_path_index, os.path.isfile(os.path.join(self.test_dir, "index.rst")))

    def test_antiweb(self):
        compare_path_small_testfile = os.path.join("unittest","small_testfile.rst")
        self.test_args = ['antiweb.py', os.path.join(self.test_dir, "small_testfile.py")]

        with patch.object(sys, 'argv', self.test_args):
            self.functional("", "small_testfile.rst", compare_path_small_testfile, main())
            self.file_not_exist(os.path.join(self.test_dir, "index.rst"))

    def test_antiweb_r_i_o(self):
        compare_path_small_testfile = os.path.join("unittest","docs","small_testfile.rst")
        compare_path_index = os.path.join("unittest","docs","index.rst")
        directory = "docs"
        self.test_args = ['antiweb.py', '-i', "-o"+directory, "-r", os.path.join(self.test_dir)]

        with patch.object(sys, 'argv', self.test_args):
            self.functional(directory, "small_testfile.rst", compare_path_small_testfile, main())
            self.functional(directory, "index.rst", compare_path_index, os.path.isfile(os.path.join(self.test_dir, directory, "index.rst")))

    def test_antiweb_r_i(self):
        compare_path_small_testfile = os.path.join("unittest","small_testfile.rst")
        compare_path_index = os.path.join("unittest","index.rst")
        self.test_args = ['antiweb.py', '-i', "-r", os.path.join(self.test_dir)]

        with patch.object(sys, 'argv', self.test_args):
            self.functional("", "small_testfile.rst", compare_path_small_testfile, main())
            self.functional("", "index.rst", compare_path_index, os.path.isfile(os.path.join(self.test_dir, "index.rst")))

    def test_antiweb_r_o(self):
        compare_path_small_testfile = os.path.join("unittest", "docs", "small_testfile.rst")
        directory = "docs"
        self.test_args = ['antiweb.py',"-o"+directory, "-r", os.path.join(self.test_dir)]

        with patch.object(sys, 'argv', self.test_args):
            self.functional(directory, "small_testfile.rst", compare_path_small_testfile, main())
            self.file_not_exist(os.path.join(self.test_dir, directory, "index.rst"))

    def test_antiweb_r(self):
        compare_path_small_testfile = os.path.join("unittest", "docs", "small_testfile.rst")
        self.test_args = ['antiweb.py', "-r", os.path.join(self.test_dir)]

        with patch.object(sys, 'argv', self.test_args):
            self.functional("", "small_testfile.rst", compare_path_small_testfile, main())
            self.file_not_exist(os.path.join(self.test_dir, "index.rst"))

    def tearDown(self):

        shutil.rmtree(self.test_dir)

if __name__ == '__main__':
    unittest.main()