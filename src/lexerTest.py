from lex import *
import sys

def main():
    print("Mini Java Compiler - Lexer Test")

    if len(sys.argv) != 2:
        sys.exit("Error: Compiler needs source file as argument.")

    with open(sys.argv[1], 'r') as f:
        buffer = f.read()
    lexer = Lexer(buffer)

    filler = ""

    # Token stream test
    print(f"{filler:-<50}\nToken Stream Test")
    # for token in lexer.tokens():
    #     print(token)
    tokens = lexer.tokens(ignore=True)
    while True:
        try:
            print(next(tokens))
        except StopIteration:
            break


if __name__ == '__main__':
    sys.argv = ["./lexerTest.py", "../test/case1/Main.java"]
    main()
