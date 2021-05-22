from ast import *
from mapper import code_mapper as _code_mapper


def compare(a, b):
	mark = {
		"byte": 0,
		"short": 0,
		"int": 0,
		"long": 1,
		"float": 2,
		"double": 3,
	}
	if isinstance(a, str) and isinstance(b, str):
		if mark.get(a, None) is not None and mark.get(b, None) is not None:
			if mark[a] == mark[b] == 0:
				return "int"
			elif mark[a] > mark[b]:
				return a
			else:
				return b
		return NotImplemented


class Semantic:
	def __init__(self, ast, symbolTable):
		self.ast = ast
		self.symbolTable = symbolTable
		self.identifier_variable = {}
		self.identifier_function = {}

	def analyze(self):
		self.traverse(self.ast)
		return self.ast

	def traverse(self, t):
		#################################
		#   check function is declared?
		#       callTree kid:
		#           *idTree
		#################################
		if isinstance(t, callTree):
			identifier_name, identifier_type = self.traverse(t.getKid(1))
			if identifier_type is None and identifier_name not in _code_mapper.IGNORE:
				raise Exception("Error: Function not found '%s'" % identifier_name)
			else:
				for tree in t.getKids():
					if tree is not t.getKid(1):
						self.traverse(tree)
			return [identifier_name, identifier_type]
		#################################
		#   check function is declared twice?
		#       declrTree kid:
		#           *typeTree
		#           *idTree
		#           *funcHead
		#           *block
		#################################
		elif isinstance(t, funcDeclTree):
			identifier_name, identifier_type = self.traverse(t.getKid(2))

			if identifier_name in self.identifier_function:
				raise Exception("Error: Function '%s' is declared twice." %identifier_name)
			else:
				self.identifier_function[identifier_name] = identifier_type

			for tree in t.getKids():
				if tree is not t.getKid(2):
					self.traverse(tree)
		#################################
		#   check variable is declared?
		#   check variable is declared twice?
		#       declrTree kid:
		#           *typeTree
		#           *idTree
		#################################
		elif isinstance(t, declrTree):
			identifier_name, identifier_type = self.traverse(t.getKid(2))

			if identifier_type is None:
				raise Exception("Error: Variable not found '%s'" %
								identifier_name)
			else:
				if identifier_name in self.identifier_variable:
					raise Exception("Error: Variable '%s' is declared twice." % identifier_name)
				else:
					if identifier_type == 'var':
						identifier_type = self.traverse(t.getKid(3))
						t.getKid(1).setType(identifier_type)
					self.identifier_variable[identifier_name] = identifier_type

			for tree in t.getKids():
				if tree is not t.getKid(2):
					self.traverse(tree)

			return identifier_type
		# check if function receive enough parameters
		# elif isinstance(t, funcHeadTree):
		#     num_of_function_variables = len(t.getKids())
		#     if num_of_function_variables is 0:
		#         return "void"
		#     else:
		#         for tree in t.getKids():
		#################################
		#   check if assign has type mismatched.
		#       assignTree kid:
		#           *idTree
		#           assign_op
		#           *expr
		#################################
		elif isinstance(t, assignTree):
			_, identifier_type_left = self.traverse(t.getKid(1))
			identifier_type_right = self.traverse(t.getKid(2))

			if identifier_type_left == identifier_type_right:
				pass
			elif identifier_type_left in ['int', 'long', 'float', 'double'] and identifier_type_right == 'int':
				pass
			elif identifier_type_left in ['long', 'float', 'double'] and identifier_type_right in ['int', 'long']:
				pass
			elif identifier_type_left in ['float', 'double'] and identifier_type_right in ['int', 'long', 'float']:
				pass
			elif identifier_type_left in ['double'] and identifier_type_right in ['int', 'long', 'float', 'double']:
				pass
			elif identifier_type_left == 'int' and identifier_type_right == 'char':
				pass
			else:
				raise Exception("Type mismatched between '%s' and '%s'" % (
					identifier_type_left, identifier_type_right))
		#################################
		#   check if relation has type mismatched.
		#       relOPTree kid:
		#           *expr
		#           rel_op
		#           *expr
		################################# 
		elif isinstance(t, relOPTree):
			identifier_type_left = self.traverse(t.getKid(1))
			identifier_type_right = self.traverse(t.getKid(2))

			if identifier_type_left != identifier_type_right:
				raise Exception("Type mismatched between '%s' and '%s'" % (
					identifier_type_left, identifier_type_right))
			else:
				return 'boolean'
		#################################
		#   check if addOPTree has type mismatched.
		#       addOPTree kid:
		#           *expr
		#           add_op
		#           *expr
		#################################
		elif isinstance(t, addOPTree):
			identifier_type_left = self.traverse(t.getKid(1))
			identifier_type_right = self.traverse(t.getKid(2))

		#################################
		#   check if multOPTree has type mismatched
		#       multOPTree kid:
		#           *expr
		#           mult_op
		#           *expr
		#################################
		elif isinstance(t, multOPTree):
			identifier_type_left = self.traverse(t.getKid(1))[1]
			identifier_type_right = self.traverse(t.getKid(2))[1]

			# if identifier_type_left == 'double' and (identifier_type_right in ['double', 'float', 'long', 'int']):
			# 	return identifier_type_left
			# elif identifier_type_left == 'float' and (identifier_type_right in ['float', 'long', 'int']):
			# 	return identifier_type_left
			# elif identifier_type_left == 'long' and (identifier_type_right in ['long', 'int']):
			# 	return identifier_type_left
			# elif identifier_type_left == 'int' and identifier_type_right == 'int':
			# 	return identifier_type_left
			# else:
			# 	raise Exception(
			# 		"Type mismatched between '%s' and '%s'" % (identifier_type_left, identifier_type_right))
			try:
				return compare(identifier_type_left, identifier_type_right)
			except NotImplemented:
				raise SyntaxError(f"`{identifier_type_left}` and `{identifier_type_right}` are unsupported")

		#################################
		#################################
		#################################
		#################################
		elif isinstance(t, numberTree):
			identifier_type = "int"
			return identifier_type
		elif isinstance(t, stringTree):
			identifier_type = "string"
			return identifier_type
		elif isinstance(t, idTree):
			identifier_name, identifier_type = self.symbolTable.get_declaration_data(t.getKey())
			return identifier_name, identifier_type
		else:
			for tree in t.getKids():
				self.traverse(tree)
