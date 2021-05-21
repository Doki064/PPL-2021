from os import path
from getopt import *
from sys import argv
from lex import *
from parse import *
from codegen import *


def r2a(rpath): return path.join(path.dirname(__file__), rpath)


def section(title, work):
    print('-' * 80)
    print(title)
    work()
    print('-' * 80)


def help_text():
    def work():
        with open(r2a('./data/help.txt'), 'r') as f:
            print(f.read())
    return "Manual:", work


def token_display():
    def work():
        with open(r2a('./data/help.txt'), 'r') as f:
            print(f.read())
    return "Manual:", work


def symtable_display():
    def work():
        with open(r2a('./data/help.txt'), 'r') as f:
            print(f.read())
    return "Manual:", work


def parsetree_display():
    def work():
        with open(r2a('./data/help.txt'), 'r') as f:
            print(f.read())
    return "Manual:", work


def codegen_display():
    def work():
        with open(r2a('./data/help.txt'), 'r') as f:
            print(f.read())
    return "Manual:", work


def main():
    print("JCOSIM: Java Compiler Simulator")
    try:
        if len(argv) < 2:
            raise GetoptError('ERROR: Input file must be specified')
        options, remainder = getopt(
            argv[1:],
            'i:o:stpgc:vh',
            [
                'input',
                'output',
                'symtable',
                'token',
                'parsetree',
                'codegen'
                'ccoption',
                'verbose',
                'help',
            ])

        source = None
        exe = None
        symtable = False
        token = False
        parsetree = False
        codegen = False
        ccoption = ""

        for opt, arg in options:
            if opt in ('-h', '--help'):
                raise GetoptError('')
            elif opt in ('-i', '--input'):
                source = r2a(arg)
            elif opt in ('-o', '--output'):
                exe = r2a(arg)
            elif opt in ('-s', '--symtable'):
                symtable = True
            elif opt in ('-t', '--token'):
                token = True
            elif opt in ('-p', '--parsetree'):
                parsetree = True
            elif opt in ('-g', '--codegen'):
                codegen = True
            elif opt in ('-c', '--ccoption'):
                ccoption = arg
            elif opt in ('-v', '--verbose'):
                symtable = True
                token = True
                parsetree = True
                codegen = True

        if not source:
            raise GetoptError('ERROR: Input file must be specified')
        if not exe:
            exe = r2a(path.basename(source))

        with open(source, 'r') as f:
            buffer = f.read()
            lexer = Lexer(buffer)
            parser = Parser(lexer)
            emitter = Emitter("cast1Main")
            # p = parser.program()  # Start the parser.
            code_gen = CodeGen(parser, emitter)
            code_gen.generate_code()
            print(code_gen.emitter.code)
            print("Parsing completed.")
            if token:
                section(*token_display())
            if symtable:
                section(*symtable_display())
            if parsetree:
                section(*parsetree_display())
            if codegen:
                section(*codegen_display())

    except GetoptError as e:
        section(*help_text())
        print(e)


main()
