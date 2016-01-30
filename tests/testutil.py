#@start()
#@cstart(imports)

import os
import tempfile
import shutil

#@(imports)

#The :py:class:`get_datapath(file)` method.
#@code
#@edoc

class Directory:
    def __init__(self, dir):
        self.dir = dir

    def get_path(self, *args):
        return os.path.join(self.dir, *args)

class DataDir(Directory):
    def __init__(self, *args):
        self.data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", *args)
        super().__init__(self.data_dir)

class TempDir(Directory):
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()
        super().__init__(self.temp_dir)

    def remove_tempdir(self):
        shutil.rmtree(self.temp_dir)
