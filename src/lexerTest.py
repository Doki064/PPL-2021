from lex import *
import sys


def main():
    print("Mini Java Compiler - Lexer Test")

    if len(sys.argv) != 2:
        sys.exit("Error: Compiler needs source file as argument.")

    inputFile = sys.argv[1]    
    lexer = Lexer(inputFile)
    for token in lexer.tokens():
        print(token)

main()
