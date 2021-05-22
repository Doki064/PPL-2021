__all__ = ["CodeGen"]

try:
	from ast import addOPTree, assignTree, blockTree, callTree, declrTree, endTree, funcDeclTree, funcHeadTree, idTree, \
		ifTree, multOPTree, numberTree, programTree, relOPTree, returnTree, stringTree, typeTree, whileTree
	from mapper import code_mapper as _code_mapper
	from mapper import get_value_by_name as _get_value_by_name
except ImportError:
	from src.ast import addOPTree, assignTree, blockTree, callTree, declrTree, endTree, funcDeclTree, funcHeadTree, \
		idTree, ifTree, multOPTree, numberTree, programTree, relOPTree, returnTree, stringTree, typeTree, whileTree
	from src.mapper import code_mapper as _code_mapper
	from src.mapper import get_value_by_name as _get_value_by_name

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
	def __init__(self, ast):
		self.ast = ast

	def travel_tree(self, t, __main=False):
		if isinstance(t, programTree):
			code = ""
			for tree in t.getKids():
				code += self.travel_tree(tree)
			return code

		elif isinstance(t, funcDeclTree):
			if self.travel_tree(t.getKid(1)) + self.travel_tree(t.getKid(2)) == "void main":
				return f"int main(void) {self.travel_tree(t.getKid(4), True)}"
			code = ""
			for tree in t.getKids():
				code += self.travel_tree(tree)
			return code
		elif isinstance(t, assignTree):
			code = self.travel_tree(t.getKid(1))
			code += f" {t.getToken()} "
			code += self.travel_tree(t.getKid(2))
			return code

		elif isinstance(t, declrTree):
			datatype = self.travel_tree(t.getKid(1))
			name = self.travel_tree(t.getKid(2))
			if t.getKid(1).isArray:
				name += "[]"
			code = datatype + name
			try:
				if self.travel_tree(t.getKid(3)) in _code_mapper.INPUT_FUNC.values():
					code = (self.travel_tree(t.getKid(3))[0] + " " + name + ";\n" +
					        self.travel_tree(t.getKid(3))[1] + name + ")" + self.travel_tree(t.getKid(4)))
					return code
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
					if name in _code_mapper.MAPPER:
						name = _code_mapper.MAPPER[name]
					elif name in _code_mapper.INPUT_FUNC:
						return _code_mapper.INPUT_FUNC[name]
					elif name in _code_mapper.IGNORE:
						return ""
					code += name + "("
				else:
					if self.travel_tree(t.getKid(idx + 1)) == ";\n":
						return code + ")" + self.travel_tree(t.getKid(idx + 1))
					code += self.travel_tree(t.getKid(idx + 1))
					if idx != t.kidCount() - 1 and self.travel_tree(t.getKid(idx + 2)) != ";\n":
						code += ", "
			code += ")"
			return code

		elif isinstance(t, (addOPTree, multOPTree, relOPTree)):
			code = (f"({self.travel_tree(t.getKid(1))} "
			        f"{_get_value_by_name(t.getToken())} "
			        f"{self.travel_tree(t.getKid(2))})")
			return code

		elif isinstance(t, typeTree):
			if t.getType() in _code_mapper.TYPE_MAPPER:
				code = _code_mapper.TYPE_MAPPER[t.getType()]
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
			return code

		elif isinstance(t, stringTree):
			code = t.getValue()
			return code

		elif isinstance(t, blockTree):
			code = "\n{\n"
			for tree in t.getKids():
				code += self.travel_tree(tree)
			if __main:
				code += "return 0;\n"
			code += "}\n"
			return code

		elif isinstance(t, funcHeadTree):
			code = "("
			for idx, tree in enumerate(t.getKids()):
				code += self.travel_tree(tree)
				if isinstance(t.getKid(idx - 1), typeTree) and isinstance(t.getKid(idx), idTree):
					if t.getKid(1).isArray:
						code += "[]"
				if idx != len(t.getKids()) - 1:
					code += ", "
			code += ")"
			return code

		elif isinstance(t, ifTree):
			block_cond = self.travel_tree(t.getKids()[0])
			block_if = self.travel_tree(t.getKids()[1])
			code = "if " + block_cond + "\n"
			code += block_if + "\n"
			if len(t.getKids()) == 3:
				block_else = self.travel_tree(t.getKids()[2])
				code += "else " + block_else + "\n"
			return code

		elif isinstance(t, whileTree):
			block_cond = self.travel_tree(t.getKids()[0])
			block_while = self.travel_tree(t.getKids()[1])
			code = "while " + block_cond + "{\n"
			code += block_while + "}\n"
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
		header = """#include <stdio.h> \n#include <stdlib.h> \n#include <math.h>\n"""
		code = self.travel_tree(self.ast)
		code = "\n".join(line for line in code.split("\n") if line.strip() != "")
		return header + code[1:-1]
