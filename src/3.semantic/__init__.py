from symbol_table import *
from parse import *

class Semantic:
    def __init__(self, parser, symbolTable):
        self.ast = parser.program()
        self.symbolTable = symbolTable
        self.identifier_variable = {}
        self.identifier_function = {}

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
        #   check function is declared twice?
        #       declrTree kid:
        #           *typeTree
        #           *idTree
        #           *funcHead
        #           *block
        #################################
        elif isinstance(t, funcDeclTree):
            identifier_key = t.getKid(2).getKey()
            identifier_name, identifier_type = self.symbolTable.get_declaration_data(identifier_key)
            if identifier_name in self.identifier_function:
                raise Exception("Error: Function '%s' is declared twice." % identifier_name)
            else:
                self.identifier_function.add(identifier_name)
        #################################
        #   check variable is declared?
        #   check variable is declared twice?
        #       declrTree kid:
        #           *typeTree
        #           *idTree
        #################################
        elif isinstance(t, declrTree):
            identifier_key = t.getKid(2).getKey()
            identifier_name, identifier_type = self.symbolTable.get_declaration_data(identifier_key)
            if identifier_type is None:
                raise Exception("Error: Variable not found '%s'" % identifier_name)
            else:
                if identifier_name in self.identifier_variable:
                    raise Exception("Error: Variable '%s' is declared twice." % identifier_name)
                else:
                    self.identifier_variable.add(identifier_name)



