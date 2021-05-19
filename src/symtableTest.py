import pprint
import sys

from lex import Lexer
from symbol_table import SymbolTable


def run():
    with open(sys.argv[1], "r") as f:
        buffer = f.read()
    table = SymbolTable(Lexer(buffer))
    pprint.pprint(table, width=640)


if __name__ == '__main__':
    sys.argv = ["symtableTest.py", "../test/case1/Main.java"]
    run()
