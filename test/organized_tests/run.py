import subprocess
import os


def path_from_file(path):
    return os.path.join(os.path.realpath(os.path.dirname(__file__)), path)


def sub_dirs(rootdir):
    for file in os.listdir(rootdir):
        d = os.path.join(rootdir, file)
        if os.path.isdir(d):
            yield d


def run_test(cats=[]):
    def run_single_cat(cat):
        cat = path_from_file(cat)
        for sd in sub_dirs(cat):
            run_single_test(f'{sd}/Main.java')

    for cat in cats: run_single_cat(cat)


def run_single_test(test_path, cc=True):
    print()
    print(test_path)
    if cc:
        # want more output?
        # subprocess.run(['python', path_from_file('../../src/jcosim.py'), f'-i{test_path}', '-putag'])
        subprocess.run(['python', path_from_file('../../src/jcosim.py'), f'-i{path_from_file(test_path)}', '-u'])
    else:
        # want more output?
        # subprocess.run(['python', path_from_file('../../src/jcosim.py'), f'-i{test_path}', '-ptag'])
        subprocess.run(['python', path_from_file('../../src/jcosim.py'), f'-i{path_from_file(test_path)}'])


if __name__ == "__main__":
    e1 = 'syntax-error'
    e2 = 'semantic-error'
    w = 'work'
    run_test([e1, e2, w])
