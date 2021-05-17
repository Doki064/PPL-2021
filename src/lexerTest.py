from lex import *
import sys


def main():
    print("Mini Java Compiler")

    if len(sys.argv) != 2:
        sys.exit("Error: Compiler needs source file as argument.")
    with open(sys.argv[1], 'r') as inputFile:
        input = inputFile.read()

        lexer = Lexer(input)
        while lexer.peek() != '\0':
            print(lexer.curChar)
            lexer.nextChar()


main()
