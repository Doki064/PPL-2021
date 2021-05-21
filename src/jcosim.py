from os import path
from getopt import *
from sys import argv
from lex import *
from parse import *
from codegen import *


def fRel(rpath): return path.join(path.dirname(__file__), rpath)


def main():
    print("Mini Java Compiler")
    try:
        if len(argv) < 2:
            raise GetoptError('')
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
    
    except GetoptError:
        with open(fRel('./data/help.txt'), 'r') as f:
            print(f.read())

    # print('OPTIONS   :', options)

    # for opt, arg in options:
    #     if opt in ('-o', '--output'):
    #         output_filename = arg
    #     elif opt in ('-v', '--verbose'):
    #         verbose = True
    #     elif opt == '--version':
    #         version = arg

    # print('VERSION   :', version)
    # print('VERBOSE   :', verbose)
    # print('OUTPUT    :', output_filename)
    # print('REMAINING :', remainder)
#    if len(sys.argv) != 2:
#         sys.exit("Error: Compiler needs source file as argument.")
#     with pathlib.Path(sys.argv[1]).open(mode="r") as f:
#         buffer = f.read()

#     # Initialize the lexer and parser.
#     lexer = Lexer(buffer)
#     parser = Parser(lexer)
#     emitter = Emitter("cast1Main")
#     # p = parser.program()  # Start the parser.
#     code_gen = CodeGen(parser, emitter)
#     code_gen.generate_code()
#     print(code_gen.emitter.code)
#     print("Parsing completed.")


main()
