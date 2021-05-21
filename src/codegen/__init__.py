try:
    from ast import *
    from lex import *
except ImportError:
    from src.ast import *
    from src.lex import *


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


MAPPER = {
    "Math.PI": "M_PI",
    "Math.pow": "pow",
    "Math.sqrt": "sqrt",
    "Math.abs": "abs",
    "System.out.println": "println",
    "System.out.printf": "printf",
}

INPUT_FUNC = {
    "scanner.nextDouble": ("double", "scanf(\"%lf\", &"),
    "scanner.nextFloat": ("float", "scanf(\"%f\", &"),
    "scanner.nextInt": ("int", "scanf(\"%d\", &"),
}

TYPE_MAPPER = {
    "String": "char*"
}

IGNORE = ["Scanner", "scanner.close"]


class CodeGen:
    def __init__(self, parser, emitter):
        self.ast = parser.program()
        self.emitter = emitter
        header = """#include <stdio.h> \n#include <math.h>"""
        self.codegen = ""
        self.emitter.emitLine(header)

    def travel_tree(self, t):
        if isinstance(t, (programTree, funcDeclTree)):
            code = ""
            for tree in t.getKids():
                code += self.travel_tree(tree)
            return code

        elif isinstance(t, assignTree):
            code = ""
            code += self.travel_tree(t.getKid(1)) + " "
            code += t.getToken() + " "
            code += self.travel_tree(t.getKid(2)) + " "
            return code

        elif isinstance(t, declrTree):
            datatype = self.travel_tree(t.getKid(1)) + " "
            name = self.travel_tree(t.getKid(2)) + " "
            code = datatype + name
            try:
                if self.travel_tree(t.getKid(3)) in INPUT_FUNC.values():
                    return (f"{self.travel_tree(t.getKid(3))[0]} {name}\n"
                            f"{self.travel_tree(t.getKid(3)[1]) + name})"
                            f"{self.travel_tree(t.getKid(4))}")
                if self.travel_tree(t.getKid(3)) == "":
                    return "\n"
                if self.travel_tree(t.getKid(3)) == ";\n":
                    return code + self.travel_tree(t.getKid(3))
                code += f" = {self.travel_tree(t.getKid(3))}"
            except TypeError:
                pass
            try:
                code += self.travel_tree(t.getKid(4))
            except TypeError:
                pass
            return code

        elif isinstance(t, callTree):
            code = ""
            for idx, kid in enumerate(t.getKids()):
                if idx == 0:
                    name = self.travel_tree(t.getKid(1))
                    if name in MAPPER:
                        name = MAPPER[name]
                    elif name in INPUT_FUNC:
                        return INPUT_FUNC[name]
                    elif name in IGNORE:
                        return ""
                    code += name + "("
                else:
                    if self.travel_tree(t.getKid(idx + 1)) == ";\n":
                        return code + ")" + self.travel_tree(t.getKid(idx + 1))
                    code += self.travel_tree(t.getKid(idx + 1))
                    if idx != len(t.getKids()) - 1:
                        code += ","
            code += ")"
            return code

        elif isinstance(t, (addOPTree, multOPTree, relOPTree)):
            code = self.travel_tree(t.getKid(1))
            code += token_names.get_value_by_name(t.getToken())
            code += self.travel_tree(t.getKid(2))
            return code

        elif isinstance(t, typeTree):
            if t.getType() in TYPE_MAPPER:
                code = TYPE_MAPPER[t.getType()]
            else:
                code = t.getType()
            return code + " "

        elif isinstance(t, idTree):
            name = t.getName()
            code = ""
            if name == "Math.PI":
                code += "M_PI"
            elif name == "Math.pow":
                code += "pow"
            else:
                code += name
            return code

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
            code += "}"
            return code

        elif isinstance(t, funcHeadTree):
            code = "("
            for idx, tree in enumerate(t.getKids()):
                code += self.travel_tree(tree)
                if idx != len(t.getKids())-1:
                    code += ", "
            code += ")"
            return code + " "

        elif isinstance(t, ifTree):
            blockCond = self.travel_tree(t.getKids()[0])
            blockIf = self.travel_tree(t.getKids()[1])
            code = "if (" + blockCond + ")\n "
            code += blockIf + "\n"
            if len(t.getKids()) == 3:
                blockElse = self.travel_tree(t.getKids()[2])
                code += "else\n" + blockElse + "\n "
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

        elif isinstance(t, endTree):
            return ";\n"
        else:
            if t is None:
                raise TypeError(type(t))
            raise SyntaxError(f"UwU What's dis error? {type(t)}")

    def generate_code(self):
        code = self.travel_tree(self.ast)
        self.emitter.emitLine(code[1:-1])
        # Add whitespace

