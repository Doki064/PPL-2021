from ast import *
from lex import *


class Emitter:
    def __init__(self, name):
        self.file_path = name + ".c"
        self.header = ""
        self.code = ""

    def emitLine(self, code):
        self.code += code + "\n"

    def writeFile(self):
        with open(self.file_path, "w+") as file:
            file.write(self.header + self.code)


class CodeGen:
    def __init__(self, parser, emitter):
        self.ast = parser.program()
        self.emitter = emitter
        header = """
        #include <stdio.h>
        #include <math.h>
        """
        self.codegen = ""
        self.emitter.emitLine(header)

    def travel_tree(self, t):
        if isinstance(t, (programTree,
                          callTree, declrTree, funcDeclTree, declTreeWithAssign, assignTree)):
            code = ""
            for tree in t.getKids():
                code += self.travel_tree(tree)
            return code
        elif isinstance(t, (addOPTree, multOPTree, relOPTree)):
            for name, value in token_names.Operators.items():
                if name == t.getToken():
                    code = value
                    return code

        elif isinstance(t, typeTree):
            code = token_names.KeywordsType(t.getLabel()).value
            return code + " "
        elif isinstance(t, idTree):
            code = t.getName()
            return code + " "
        elif isinstance(t, numberTree):
            code = t.getValue()
            return code + " "
        elif isinstance(t, stringTree):
            code = t.getValue()
            return code + " "
        elif isinstance(t, blockTree):
            code = "{ \n"
            for tree in t.getKids():
                code += self.travel_tree(tree)
            code += "} \n"
            return code + " "
        elif isinstance(t, funcHeadTree):
            code = "("
            for tree in t.getKids():
                code += self.travel_tree(tree)
            code += ")"
            return code + " "
        elif isinstance(t, ifTree):
            blockCond = self.travel_tree(t.getKids()[0])
            blockIf = self.travel_tree(t.getKids()[1])
            code = "if " + blockCond + "{ \n "
            code += blockIf + "} \n"
            if len(t.getKids()) == 3:
                blockElse = self.travel_tree(t.getKids()[2])
                code += "else { \n" + blockElse + "} \n "
            return code
        elif isinstance(t, whileTree):
            blockCond = self.travel_tree(t.getKids()[0])
            blockWhile = self.travel_tree(t.getKids()[1])
            code = "while " + blockCond + "{ \n "
            code += blockWhile + "} \n "
            return code
        elif isinstance(t, returnTree):
            code = "return "
            for tree in t.getKids():
                code += self.travel_tree(tree)
            return code
        else:
            raise SyntaxError("UwU What's dis error")

    def generate_code(self):
        code = self.travel_tree(self.ast)
        self.emitter.emitLine(code)
        # Add whitespace
