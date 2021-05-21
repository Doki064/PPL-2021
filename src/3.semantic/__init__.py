from symbol_table import *
from parse import *

class Semantic:
    def __init__(self, parser, symbolTable):
        self.ast = parser.program()
        self.symbolTable = symbolTable

    def traverse(self, t):
        #################################
        #   check function is declared?
        #       callTree kid:
        #           *idTree
        #################################
        if isinstance(t, callTree):
            identifier_key = t.getKid(1).getKey()
            identifier_name, identifier_type = self.symbolTable.get_declaration_data(identifier_key)
            if identifier_type is None:
                raise Exception("Error: Function not found '%s'" % identifier_name)
        #################################
        #   check variable is declared?
        #       declrTree kid:
        #           *typeTree
        #           *idTree
        #################################
        elif isinstance(t, declrTree):
            identifier_key = t.getKid(2).getKey()
            identifier_name, identifier_type = self.symbolTable.get_declaration_data(identifier_key)
            if identifier_type is None:
                raise Exception("Error: Variable not found '%s'" % identifier_name)


