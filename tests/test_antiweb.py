#@start()
#@cstart(imports)

import unittest
from unittest.mock import patch
from antiweb import main
from antiweb_lib.readers.GenericReader import GenericReader
import sys
import os
import shutil
from tests.testutil import TempDir
from tests.testutil import DataDir
import time
from multiprocessing import Process

sys.path.append("..")


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
        self.doc_dir = "docs"
        self.source_dir = "sources"
        self.temp_dir = TempDir()
        self.data_dir = DataDir("unittest")
        self.origin_path = self.data_dir.get_path("small_testfile.py")
        self.empty_origin_path = self.data_dir.get_path("empty.py")

        self.destination_path = self.temp_dir.get_path(self.source_dir, "small_testfile.py")
        self.empty_destination_path = self.temp_dir.get_path(self.source_dir, "empty.py")

        self.temp_dir.copy_file(self.origin_path, self.destination_path)
        self.temp_dir.copy_file(self.empty_origin_path, self.empty_destination_path)
    #@edoc

    #The :py:class:`functional(self, directory, filename, compare_path, assert_input)` class tests if antiweb was fully executed and if the files were created in the correct a
    #@code
    def functional(self, directory, filename, compare_path, assert_input):
        self.assertTrue(assert_input)

        self.compare(directory, filename, compare_path)
    #@edoc

    #In some cases a file should not be created, the :py:class:`file_not_exist(self, path)` class will verify that expectation
    #@code
    def file_not_exist(self, path):

        self.assertFalse(os.path.isfile(path))

    def compare(self, directory, filename, compare_path):

        with open(self.temp_dir.get_path(directory, filename)) as output:
            antiweb_output = output.readlines()
        with open(compare_path) as compare:
            antiweb_compare = compare.readlines()
        self.assertEqual(antiweb_output, antiweb_compare)
    #@edoc
    #@(preparation)

    #@start(testcase)
    #This is one of eight tests that will be performed. ``compare_path_small_testfile`` is the path to the file to compare the output with.
    #The arguments which would normally be set in the command prompt are set using ``patch.object` wich is imported from :py:class:`unittest.mock`
    #After the arguments are set :py:class:``self.functional`` is called to compare the expectation with the actual output.

    #@code

    def test_antiweb_o(self):
        compare_path_small_testfile = self.data_dir.get_path("small_testfile.rst")
        self.test_args = ['antiweb.py', "-o", self.temp_dir.get_path(self.doc_dir),
                          self.destination_path]

        with patch.object(sys, 'argv', self.test_args):
            self.functional("", os.path.join(self.doc_dir, "small_testfile.rst"), compare_path_small_testfile, main())

    def test_antiweb_o_relative_path(self):
        compare_path_small_testfile = self.data_dir.get_path("small_testfile.rst")

        relative_path = self.temp_dir.get_relative_path(self.doc_dir)

        self.test_args = ['antiweb.py', "-o",relative_path,
                            self.destination_path]

        with patch.object(sys, 'argv', self.test_args):
            self.functional("", os.path.join(self.doc_dir, "small_testfile.rst"), compare_path_small_testfile,
                            main())

    #@edoc
    #@(preparation)

    def test_antiweb_o_file(self):
        output_file_name = "small_testfile.rst"

        compare_path_small_testfile = self.data_dir.get_path(output_file_name)
        self.test_args = ['antiweb.py', "-o", self.temp_dir.get_path(output_file_name), self.destination_path]

        with patch.object(sys, 'argv', self.test_args):
            self.functional("", output_file_name, compare_path_small_testfile, main())

    def test_antiweb(self):
        compare_path_small_testfile = self.data_dir.get_path("small_testfile.rst")
        self.test_args = ['antiweb.py', self.destination_path]

        with patch.object(sys, 'argv', self.test_args):
            self.functional(self.source_dir, "small_testfile.rst", compare_path_small_testfile, main())

    def test_antiweb_relative_path(self):
        compare_path_small_testfile = self.data_dir.get_path("small_testfile.rst")
        self.test_args = ['antiweb.py', self.temp_dir.get_relative_path(self.destination_path)]

        with patch.object(sys, 'argv', self.test_args):
            self.functional(self.source_dir, "small_testfile.rst", compare_path_small_testfile, main())

    def test_antiweb_r_o(self):
        compare_path_small_testfile = self.data_dir.get_path("docs","small_testfile.rst")
        self.test_args = ['antiweb.py',"-o" , self.temp_dir.get_path(self.doc_dir), "-r", self.temp_dir.get_path()]

        with patch.object(sys, 'argv', self.test_args):
            self.functional(self.doc_dir, "small_testfile.rst", compare_path_small_testfile, main())

    def test_antiweb_r_absolute(self):
        compare_path_small_testfile = self.data_dir.get_path("small_testfile.rst")
        self.test_args = ['antiweb.py',"-r", self.temp_dir.get_path()]

        with patch.object(sys, 'argv', self.test_args):
            self.functional("", "small_testfile.rst", compare_path_small_testfile, main())

    def test_antiweb_r_relative_path(self):
        compare_path_small_testfile = self.data_dir.get_path("small_testfile.rst")
        self.test_args = ['antiweb.py', "-r", self.temp_dir.get_relative_path()]

        with patch.object(sys, 'argv', self.test_args):
            self.functional("", "small_testfile.rst", compare_path_small_testfile, main())

    def test_antiweb_r_o_absolute_path(self):
        compare_path_small_testfile = self.data_dir.get_path( "docs", "small_testfile.rst")
        self.test_args = ['antiweb.py',"-o", self.temp_dir.get_path(self.doc_dir), "-r", self.temp_dir.get_path()]

        with patch.object(sys, 'argv', self.test_args):
            self.functional(self.doc_dir, "small_testfile.rst", compare_path_small_testfile, main())

    def test_antiweb_r_o_relative_path(self):
        compare_path_small_testfile = self.data_dir.get_path( "docs", "small_testfile.rst")

        self.test_args = ['antiweb.py',"-o", self.temp_dir.get_relative_path(self.doc_dir), "-r", self.temp_dir.get_relative_path()]

        with patch.object(sys, 'argv', self.test_args):
            self.functional(self.doc_dir, "small_testfile.rst", compare_path_small_testfile, main())

    def test_antiweb_r_absolute_path(self):
        compare_path_small_testfile = self.data_dir.get_path( "docs", "small_testfile.rst")
        self.test_args = ['antiweb.py', "-r", self.temp_dir.get_path()]

        with patch.object(sys, 'argv', self.test_args):
            self.functional("", "small_testfile.rst", compare_path_small_testfile, main())

    def test_antiweb_r_relative_path(self):
        compare_path_small_testfile = self.data_dir.get_path( "docs", "small_testfile.rst")
        self.test_args = ['antiweb.py', "-r", self.temp_dir.get_relative_path()]

        with patch.object(sys, 'argv', self.test_args):
            self.functional("", "small_testfile.rst", compare_path_small_testfile, main())

    def test_antiweb_r_o_no_argument(self):
        previ_dir = os.getcwd()
        os.chdir(self.temp_dir.get_relative_path())
        compare_path_small_testfile = self.data_dir.get_path("docs","small_testfile.rst")
        self.test_args = ['antiweb.py',"-o" , self.doc_dir, "-r"]

        with patch.object(sys, 'argv', self.test_args):
            self.functional(self.doc_dir, "small_testfile.rst", compare_path_small_testfile, main())

        os.chdir(previ_dir)

    def test_antiweb_r_no_argument(self):
        previ_dir = os.getcwd()
        os.chdir(self.temp_dir.get_relative_path())
        compare_path_small_testfile = self.data_dir.get_path("docs","small_testfile.rst")
        self.test_args = ['antiweb.py', "-r"]

        with patch.object(sys, 'argv', self.test_args):
            self.functional("", "small_testfile.rst", compare_path_small_testfile, main())

        os.chdir(previ_dir)

    # First goal: do not crash on this empty file;
    # Second Goal: do not create any files
    def test_antiweb_empty_file(self):
        self.test_args = ['antiweb.py', self.temp_dir.get_path("empty.py")]

        with patch.object(sys, 'argv', self.test_args):
            self.file_not_exist(self.temp_dir.get_path("empty.rst"))

    def test_antiweb_r_o_d(self):

        self.test_args = ['antiweb.py', "-o", self.temp_dir.get_path(self.source_dir), "-r",
                          self.temp_dir.get_path(self.source_dir), "-d"]

        with patch.object(sys, 'argv', self.test_args):

            #fd needed to set the stdin of the child process to the same stdin as the parent process
            fd = sys.stdin.fileno()
            log_file = self.temp_dir.get_path("logfile.out")

            p = Process(target=antiweb_process, args=(fd, log_file))

            p.start()
            time.sleep(3)

            with open(self.destination_path, 'w') as input_file:
                input_file.write('#@start()\n')
                input_file.write('#@include(new_block)\n')
                input_file.write('#@start(new_block)\n')
                input_file.write('new_text\n')
                input_file.write('#@(new_block)\n')

            time.sleep(3)
            p.terminate()
            p.join(3)

            created_file = self.temp_dir.get_path(self.source_dir, "small_testfile.rst")

            with open(created_file) as output:
                antiweb_output = output.readlines()

            with open(log_file) as logger:
                lines = logger.readlines()

            for line in lines:
                print(line)

            #the last_line should always contain information about the ignored change of the created file
            last_line = lines[-1]

            expected_info = "Ignored change: " + created_file + " [modified]\n"

            self.assertTrue(last_line.__contains__(expected_info))
            self.assertEqual(antiweb_output, ["new_text"])


    def tearDown(self):
        self.temp_dir.remove_tempdir()


def antiweb_process(fd, log_file):
    #we need to duplicate the file descriptor and reset the stdin for a childprocess
    #now the the parent and child process read from the same stdin
    sys.stdin = os.fdopen(os.dup(fd))

    #need to use a file here, as string streams are not serializable but have to be used by different processes
    with open(log_file, "w") as logger:
        sys.stdout = logger
        main()


class Test_Antiweb_rst(unittest.TestCase):

    #@start(preparation)
    #This function will be called before each Test. It copies the file to process into the temp directory of the test
    #@code
    def setUp(self):
        self.doc_dir = "docs"
        self.temp_dir = TempDir()
        self.data_dir = DataDir("unittest_rst")
        self.origin_path = self.data_dir.get_path("ein_rst.rst")
        self.destination_path = self.temp_dir.get_path("ein_rst.rst")

        shutil.copyfile(self.origin_path, self.destination_path)
    #@edoc

    #The :py:class:`functional(self, directory, filename, compare_path, assert_input)` class tests if antiweb was fully executed and if the files were created in the correct a
    #@code
    def functional(self, directory, filename, compare_path, assert_input):

        self.assertTrue(assert_input)

        self.compare(directory, filename, compare_path)
    #@edoc

    #In some cases a file should not be created, the :py:class:`file_not_exist(self, path)` class will verify that expectation
    #@code
    def file_not_exist(self, path):

        self.assertFalse(os.path.isfile(path))

    def compare(self, directory, filename, compare_path):

        with open(self.temp_dir.get_path(directory, filename)) as output:
            antiweb_output = output.readlines()
        with open(compare_path) as compare:
            antiweb_compare = compare.readlines()
        self.assertEqual(antiweb_output, antiweb_compare)
    #@edoc
    #@(preparation)

    #@start(testcase)
    #This is one of eight tests that will be performed. ``compare_path_small_testfile`` is the path to the file to compare the output with.
    #The arguments which would normally be set in the command prompt are set using ``patch.object` wich is imported from :py:class:`unittest.mock`
    #After the arguments are set :py:class:``self.functional`` is called to compare the expectation with the actual output.

    def test_antiweb_rst(self):
        compare_path_small_testfile = self.data_dir.get_path("ein_rst_docs.rst")
        self.test_args = ['antiweb.py', self.temp_dir.get_path("ein_rst.rst")]

        with patch.object(sys, 'argv', self.test_args):
            self.functional("", "ein_rst_docs.rst", compare_path_small_testfile, main())

    def test_antiweb_rst_o_directory(self):
        compare_path_small_testfile = self.data_dir.get_path("ein_rst_docs.rst")
        self.test_args = ['antiweb.py', "-o", self.temp_dir.get_path(self.doc_dir), self.temp_dir.get_path("ein_rst.rst")]

        with patch.object(sys, 'argv', self.test_args):
            self.functional("", os.path.join(self.doc_dir, "ein_rst_docs.rst"), compare_path_small_testfile, main())

    def test_antiweb_rst_o_file(self):
        compare_path_small_testfile = self.data_dir.get_path("ein_rst_docs.rst")
        self.test_args = ['antiweb.py', "-o", self.temp_dir.get_path("ein_rst_docs.rst"), self.temp_dir.get_path("ein_rst.rst")]

        with patch.object(sys, 'argv', self.test_args):
            self.functional("", "ein_rst_docs.rst", compare_path_small_testfile, main())

    def test_antiweb_rst_absolute_path(self):
        compare_path_small_testfile = self.data_dir.get_path("ein_rst_docs.rst")
        self.test_args = ['antiweb.py', self.temp_dir.get_path("ein_rst.rst")]

        with patch.object(sys, 'argv', self.test_args):
            self.functional("", "ein_rst_docs.rst", compare_path_small_testfile, main())

    def test_antiweb_rst_relative_path(self):
        compare_path_small_testfile = self.data_dir.get_path("ein_rst_docs.rst")
        self.test_args = ['antiweb.py', self.temp_dir.get_relative_path("ein_rst.rst")]

        with patch.object(sys, 'argv', self.test_args):
            self.functional("", "ein_rst_docs.rst", compare_path_small_testfile, main())

    def test_antiweb_rst_o(self):
        compare_path_small_testfile = self.data_dir.get_path("ein_rst_docs.rst")
        self.test_args = ['antiweb.py', "-o", self.temp_dir.get_path(self.doc_dir), self.temp_dir.get_path("ein_rst.rst")]

        with patch.object(sys, 'argv', self.test_args):
            self.functional("", os.path.join(self.doc_dir, "ein_rst_docs.rst"), compare_path_small_testfile, main())

    def test_antiweb_rst_r_o(self):
        compare_path_small_testfile = self.data_dir.get_path("docs","ein_rst.rst")
        self.test_args = ['antiweb.py', "-o" , self.temp_dir.get_path(self.doc_dir), "-r", self.temp_dir.get_path()]

        with patch.object(sys, 'argv', self.test_args):
            self.functional(self.doc_dir, "ein_rst_docs.rst", compare_path_small_testfile, main())

    def test_antiweb_rst_r(self):
        compare_path_small_testfile = self.data_dir.get_path("ein_rst_docs.rst")
        self.test_args = ['antiweb.py', "-r", self.temp_dir.get_path()]

        with patch.object(sys, 'argv', self.test_args):
            self.functional("", "ein_rst_docs.rst", compare_path_small_testfile, main())

    def test_antiweb_rst_r(self):
        compare_path_small_testfile = self.data_dir.get_path( "docs", "ein_rst.rst")
        self.test_args = ['antiweb.py', "-r", self.temp_dir.get_path()]

        with patch.object(sys, 'argv', self.test_args):
            self.functional("", "ein_rst_docs.rst", compare_path_small_testfile, main())

    def tearDown(self):
        self.temp_dir.remove_tempdir()

class Test_CSharp(unittest.TestCase):
    #@start(csharp_preparation)
    #This function will be called before each Test. It copies the files to process into the temp directory of the test.
    #@code
    def setUp(self):
        self.doc_dir = "docs"
        self.temp_dir = TempDir()
        self.data_dir = DataDir("unittest_csharp")

        shutil.copyfile(self.data_dir.get_path("test_simple.cs"), self.temp_dir.get_path("test_simple.cs"))
        shutil.copyfile(self.data_dir.get_path("test_xml.cs"), self.temp_dir.get_path("test_xml.cs"))
    #@edoc

    #The :py:class:`functional(self, directory, filename, compare_path, assert_input)` class tests if antiweb was fully executed and if the files were created correctly.
    #@code
    def functional(self, directory, filename, compare_path, assert_input):
        self.assertTrue(assert_input)
        self.compare(directory, filename, compare_path)
    #@edoc

    # In some cases a file should not be created
    #@code
    def file_not_exist(self, path):
        self.assertFalse(os.path.isfile(path))

    def compare(self, directory, filename, compare_path):
        with open(self.temp_dir.get_path(directory, filename)) as output:
            antiweb_output = output.readlines()
        with open(compare_path) as compare:
            antiweb_compare = compare.readlines()
        self.assertEqual(antiweb_output, antiweb_compare)
    #@edoc
    #@(csharp_preparation)

    def test_simple(self):
        compare_path_small_testfile = self.data_dir.get_path("test_simple.rst")
        self.test_args = ['antiweb.py', self.temp_dir.get_path("test_simple.cs")]

        with patch.object(sys, 'argv', self.test_args):
            self.functional("", "test_simple.rst", compare_path_small_testfile, main())

    def test_xml_tags(self):
        compare_path_small_testfile = self.data_dir.get_path("test_xml.rst")
        self.test_args = ['antiweb.py', self.temp_dir.get_path("test_xml.cs")]

        with patch.object(sys, 'argv', self.test_args):
            self.functional("", "test_xml.rst", compare_path_small_testfile, main())

    def tearDown(self):
        self.temp_dir.remove_tempdir()

class Test_Antiweb_Xml(unittest.TestCase):

    def setUp(self):
        self.doc_dir = "docs"
        self.temp_dir = TempDir()
        self.data_dir = DataDir("unittest_xml")
        self.origin_path = self.data_dir.get_path("test_xml.xml")
        self.destination_path = self.temp_dir.get_path("test_xml.xml")

        shutil.copyfile(self.origin_path, self.destination_path)

    def compare(self, directory, filename, compare_path):
        with open(self.temp_dir.get_path(directory, filename)) as output:
            antiweb_output = output.readlines()
        with open(compare_path) as compare:
            antiweb_compare = compare.readlines()
        self.assertEqual(antiweb_output, antiweb_compare)

    def functional(self, directory, filename, compare_path, assert_input):
        self.assertTrue(assert_input)
        self.compare(directory, filename, compare_path)

    def test_xml(self):
        compare_path = self.data_dir.get_path("test_xml.rst")
        self.test_args = ['antiweb.py', self.destination_path]

        with patch.object(sys, 'argv', self.test_args):
            self.functional("", "test_xml.rst", compare_path, main())

class Test_GenericReader(unittest.TestCase):

    def setUp(self):
        self.reader = GenericReader(["//",";"],[("/*", "*/"),("#","@")])

    def test_GenericReader_Creation(self):
        self.test_args = ['antiweb.py', "C:\\Users\\z003jkbt\\Documents\\waas\\testfile.py"]

        with patch.object(sys, 'argv', self.test_args):
            self.assertEqual(self.reader.single_comment_markers, ["//",";"])
            self.assertEqual(self.reader.block_comment_markers, [("/*", "*/"),("#","@")])



if __name__ == '__main__':
    unittest.main()
