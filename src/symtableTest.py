if __name__ == '__main__':
    from lex import Lexer
    from symbol_table import SymbolTable
    import pprint

    with open("../test/case1/Main.java", "r") as f:
        buffer = f.read()
        table = SymbolTable(Lexer(buffer))
        pprint.pprint(table, width=640)
        print("----------------------------------------------------------")

    with open("../test/case2/Main.java", "r") as f:
        buffer = f.read()
        table = SymbolTable(Lexer(buffer))
        pprint.pprint(table, width=640)
        print("----------------------------------------------------------")

    with open("../test/case3/Main.java", "r") as f:
        buffer = f.read()
        table = SymbolTable(Lexer(buffer))
        pprint.pprint(table, width=640)
        print("----------------------------------------------------------")
