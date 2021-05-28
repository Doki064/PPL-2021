from distutils.ccompiler import new_compiler
from glob import glob
from os import remove, path


class CCompiler:
    def __init__(self, src_file, exe_file=None):
        self.src_file = src_file
        self.exe_file = exe_file
        if not self.exe_file:
            self.exe_file = self.src_file.split('.')[0]
        self.compiler = new_compiler()

    def clean(self, include_exe=False):
        for f in glob('*.o*'):
            remove(f)
        if (include_exe):
            for f in glob(f'{self.exe_file}.exe'):
                remove(f)
            for f in glob(self.exe_file):
                remove(f)

    def exe(self, clean=True):
        self.obj()
        # libraries=['m'] <=> -lm : link with math library
        self.compiler.link_executable(glob('*.o*'), libraries=['m'], output_progname=self.exe_file)
        if clean:
            self.clean()

    def obj(self):
        self.compiler.compile([self.src_file])
