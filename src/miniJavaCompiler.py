import json
import pathlib
import sys

try:
    from codegen import CodeGen
    from lex import Lexer
    from parse import Parser
    from symbol_table import SymbolTable
except ImportError:
    from src.codegen import CodeGen
    from src.lex import Lexer
    from src.parse import Parser
    from src.symbol_table import SymbolTable


def main():
    print("Mini Java Compiler")

    if len(sys.argv) < 2:
        sys.exit("Error: Compiler needs source file as argument.")

    with pathlib.Path(sys.argv[1]).resolve().open(mode="r") as f:
        buffer = f.read()

    target_dir = pathlib.Path(__file__).parent.joinpath("../dumps")
    target_dir.mkdir(parents=True, exist_ok=True)

    print(f"{'':-<50}\nLexer Test")

    lexer = Lexer(buffer)

    with target_dir.joinpath("./tokens.txt").open("w") as f:
        print(f"{'Position':10}{'Stream':<10}{'Token name':20}{'Value':20}", file=f)
        for token in lexer.tokens():
            print(token, file=f)
    print("Lexing completed.")

    print(f"{'':-<50}\nSymbol Table Test")
    symtable = SymbolTable(lexer)
    with target_dir.joinpath("./symtable.json").open("w") as f:
        json.dump(symtable.data, f, indent=4)
    print("Symbol table completed.")

    print(f"{'':-<50}\nParser Test")
    parser = Parser(lexer)
    ast = parser.program()
    print("Parsing completed.")

    print(f"{'':-<50}\nCode Generator Test")
    code_gen = CodeGen(ast)
    code = code_gen.generate_code()
    with target_dir.joinpath("./output.c").open("w") as f:
        print(code, file=f)
    print("Code generation completed.")


if __name__ == "__main__":
    # sys.argv = ["", "../test/case5/Main.java"]
    main()
