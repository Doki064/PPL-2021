import pathlib

from lex import *
from parse import *
from codegen import *


def main():
    print("Mini Java Compiler")

    if len(sys.argv) != 2:
        sys.exit("Error: Compiler needs source file as argument.")
    with pathlib.Path(sys.argv[1]).open(mode="r") as f:
        buffer = f.read()

    # Initialize the lexer and parser.
    lexer = Lexer(buffer)
    parser = Parser(lexer)
    emitter = Emitter("cast1Main")
    # p = parser.program()  # Start the parser.
    code_gen = CodeGen(parser, emitter)
    code_gen.generate_code()
    print(code_gen.emitter.code)
    print("Parsing completed.")


sys.argv = ["", "../test/case1/Main.java"]
main()
