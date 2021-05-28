from getopt import getopt, GetoptError
from pathlib import Path
from sys import argv
from sys import exit

from pydot import Dot, Node, Edge

from c_compiler import CCompiler, CustomGCC
from codegen import CodeGen
from lex import Lexer
from parse import Parser
from semantic import Semantic
from symbol_table import SymbolTable
import os

os.environ["PATH"] += os.pathsep + os.path.abspath("./lib/bin")


def section(title, work):
    print('-' * 80)
    print(title)
    work()
    print('-' * 80)


def help_text():
    def work():
        with Path.joinpath(Path(__file__).parent, Path('data/help.txt')).resolve().open('r') as f:
            print(f.read())

    return "Manual:", work


def token_display(lexer):
    def work():
        lexer.reset()
        tokens = '\n'.join(
            map(str, list(lexer.tokens(ignore=False))))
        print(tokens)
        with Path('tokens.txt').resolve().open('w') as f:
            f.write(tokens)

    return "Tokens:", work


def symtable_display(stb):
    from json import dump
    from pprint import pprint

    def work():
        pprint(stb.data, indent=4, sort_dicts=False)
        with Path("symtable.json").resolve().open("w") as f:
            dump(stb.data, f, indent=4)

    return "Symbol Table:", work


def parsetree_display(program_tree, outputFilePath):
    def work():
        graph = Dot(graph_name='Parse Tree', graph_type='graph')

        def start_graph(g, node, parent_node_name=None):
            g.add_node(Node(name=node.getNodeNum(), shape='plaintext', label=node.getLabel()))
            if parent_node_name: g.add_edge(Edge(parent_node_name, node.getNodeNum()))
            if len(node.getKids()) > 0:
                for kid in node.getKids(): start_graph(g, kid, node.getNodeNum())
            else:
                g.add_node(Node(name=f'{node.getNodeNum()}_content', shape='plaintext', label=node.getContent()))
                g.add_edge(Edge(node.getNodeNum(), f'{node.getNodeNum()}_content'))

        start_graph(graph, program_tree)
        graph.write_png(outputFilePath if outputFilePath[-4:] == '.png' else outputFilePath + '.png')

    return "Generating Parse Tree . . .", work


def gencode_display(code, exe):
    def work():
        print(code)
        with Path(f"{exe}.c").resolve().open("w") as f:
            f.write(code)

    return "Generating code . . .", work


def clean_display(files):
    def work():
        print(files)

    return "Cleaning files", work


def native_compile_display(code, exe, cc):
    def work():
        # Save code to source file first
        with open(f"{exe}.c", "w") as f:
            f.write(code)
        # Call native C compiler
        try:
            if cc:
                cc_class = CustomGCC
            else:
                cc_class = CCompiler
            cc_class(src_file=f"{exe}.c", exe_file=exe).exe()
        except Exception as e:
            print(e)
        finally:
            # Remove source code after finish
            if Path(f'{exe}.c').exists():
                Path(f'{exe}.c').unlink()

    return "Compiling with native C compiler", work


def main():
    print("JCOSIM: Java Compiler Simulator")
    try:
        if len(argv) < 2:
            raise GetoptError('ERROR: Input file must be specified')
        options, remainder = getopt(
            argv[1:],
            'i:o:stuapgc:vh',
            [
                'input=',
                'output=',
                'symtable',
                'token',
                'use-gcc',
                'analyzedtree',
                'analy',
                'gencode',
                'clean=',
                'verbose',
                'help',
            ])

        source = None
        exe = None
        symtable = False
        token = False
        parsetree = False
        analyzedtree = False
        gencode = False
        cc = False

        for opt, arg in options:
            if opt in ('-h', '--help'):
                raise GetoptError('')
            elif opt in ('-c', '--clean'):
                clean_path = arg
                files = [
                    'tokens.txt',
                    'parsetree.png',
                    'symtable.txt',
                    f'{exe}.c',
                    f'{exe}.exe',
                    f'{exe}',
                    f'{exe}.o',
                    f'{exe}.obj'
                ]
                section(*clean_display(files))
                for file in files:
                    _path = Path(clean_path).joinpath(file).resolve()
                    if Path(_path).exists():
                        Path(_path).unlink()
                exit()
            elif opt in ('-i', '--input'):
                source = arg
            elif opt in ('-u', '--use-gcc'):
                cc = True
            elif opt in ('-o', '--output'):
                exe = arg
            elif opt in ('-s', '--symtable'):
                symtable = True
            elif opt in ('-t', '--token'):
                token = True
            elif opt in ('-p', '--parsetree'):
                parsetree = True
            elif opt in ('-a', '--analyzedtree'):
                analyzedtree = True
            elif opt in ('-g', '--gencode'):
                gencode = True
            elif opt in ('-v', '--verbose'):
                symtable = True
                token = True
                parsetree = True
                analyzedtree = True
                gencode = True

        # No source no life
        if not source:
            raise GetoptError('ERROR: Input file must be specified')

        # Smartly get exe file name
        if not exe:
            exe = Path(source).stem

        # Read Java source file
        with open(source, 'r') as f:
            buffer = f.read()

        # Lexing
        lexer = Lexer(buffer)

        # Parsing
        parser = Parser(lexer)
        program_tree = parser.program()

        # Generate symbol table
        lexer.reset()
        stb = SymbolTable(lexer)

        # Semantic
        semantic = Semantic(program_tree, stb)
        analyzed_tree = semantic.analyze()

        # Generate C code
        code_gen = CodeGen(analyzed_tree, stb)
        code = code_gen.generate_code()

        # Compile the code and output native binary
        section(*native_compile_display(code, exe, cc))

        # do things based on flags
        if token:
            section(*token_display(lexer))
        if symtable:
            section(*symtable_display(stb))
        if parsetree:
            section(*parsetree_display(program_tree, 'parsetree.png'))
        if analyzedtree:
            section(*parsetree_display(analyzed_tree, 'analyzedtree.png'))
        if gencode:
            section(*gencode_display(code, exe))

    except GetoptError as e:
        section(*help_text())
        print(e)


if __name__ == '__main__':
    main()
