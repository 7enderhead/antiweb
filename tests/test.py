import sys
import unittest
import os.path
from tests.testutil import DataDir

sys.path.append("..")

from antiweb_lib.document import WebError
from antiweb_lib.write import generate

class TestAntiWeb(unittest.TestCase):
    def check(self, fname, tokens=None):
        data_dir = DataDir("test")
        fname = data_dir.get_path(fname)

        try:
            text = generate(fname, tokens, True)
        except WebError as e:
            return e.error_list, []
        
        output = os.path.splitext(fname)[0] + ".rst"

        try:
            with open(output, "r") as f:
                cmp_text = f.read()

            return cmp_text, text
        
        except IOError:
            with open(output, "w") as f:
                f.write(text)

            return text, text
        

    def test_block1(self):
        t1, t2 = self.check("block1.c")
        self.assertEqual(t1, t2)


    def test_block2(self):
        t1, t2 = self.check("block2.c")
        self.assertEqual(t1, t2)


    def test_block3(self):
        t1, t2 = self.check("block3.c")
        self.assertEqual(t1, t2)


    def test_block4(self):
        t1, t2 = self.check("block4.c")
        self.assertEqual(t1, t2)


    def test_block5(self):
        t1, t2 = self.check("block5.c")
        self.assertEqual(t1, t2)


    def test_string_subst(self):
        t1, t2 = self.check("string_subst.c")
        self.assertEqual(t1, t2)


    def test_complex_macro(self):
        t1, t2 = self.check("complex_macro.c")
        self.assertEqual(t1, t2)


    def test_file_rstart(self):
        t1, t2 = self.check("other_file.c")
        self.assertEqual(t1, t2)


    def test_file_rstart1(self):
        t1, t2 = self.check("other_file1.c")
        self.assertEqual(t1, t2)


    def test_if1(self):
        t1, t2 = self.check("iftest1.c")
        self.assertEqual(t1, t2)


    def test_if2(self):
        t1, t2 = self.check("iftest2.c", ["show"])
        self.assertEqual(t1, t2)


    def test_if3(self):
        t1, t2 = self.check("iftest3.c", ["noshow"])
        self.assertEqual(t1, t2)

    def test_if4(self):
        t1, t2 = self.check("iftest4.c", ["show"])
        self.assertEqual(t1, t2)


    def test_named_end(self):
        t1, t2 = self.check("named_end.c")
        self.assertEqual(t1, t2)

    def test_code_prefix(self):
        t1, t2 = self.check("code_prefix.c")
        self.assertEqual(t1, t2)


    def test_indent1(self):
        t1, t2 = self.check("indent_test1.c")
        self.assertEqual(t1, t2)




if __name__ == "__main__":
    unittest.main()

    



