import pathlib

from lex import *
from parse import *


def main():
    print("Mini Java Compiler")

    if len(sys.argv) != 2:
        sys.exit("Error: Compiler needs source file as argument.")
    with pathlib.Path(sys.argv[1]).open(mode="r") as f:
        buffer = f.read()

    # Initialize the lexer and parser.
    lexer = Lexer(buffer)
    parser = Parser(lexer)

    parser.program()  # Start the parser.
    print("Parsing completed.")


main()
