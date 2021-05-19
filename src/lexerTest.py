from lex import *
import sys


def main():
    print("Mini Java Compiler - Lexer Test")

    if len(sys.argv) != 2:
        sys.exit("Error: Compiler needs source file as argument.")

    inputFile = sys.argv[1]    
    lexer = Lexer(inputFile)

    filler = ""

    # Token stream test
    print(f"{filler:-<50}\nToken Stream Test")
    # for token in lexer.tokens():
    #     print(token)
    tokens = lexer.tokens()
    while True:
        try:
            print(next(tokens))
        except StopIteration:
            break

    # Symbol table test
    print(f"{filler:-<50}\nSymbol Table Test")
    for _, v in Symbol.getSymbolsTable().items():
        print(f"{v}")
main()
