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
	__comparableTypes = {
		'int': 1,
		'long': 1,
		'byte': 1,
		'short': 1,
		'float': 1,
		'double': 1,
		'string': 2
	}

	def __init__(self, ast, symbolTable):
		self.ast = ast
		self.symbolTable = symbolTable
		self.identifier_variable = {}
		self.identifier_function = {}

	def analyze(self):
		try:
			self.traverse(self.ast)
		except Exception as e:
			print("Error. ")
			print(e)
			exit()
		return self.ast

	def traverse(self, t):
		#################################
		#   check function is declared?
		#       callTree kid:
		#           *idTree
		#################################
		if isinstance(t, callTree):
			identifier_name, identifier_type, identifier_key = self.traverse(t.getKid(1))
			if identifier_type is None and identifier_name not in _code_mapper.SUPPORTED_FUNC:
				raise Exception("Error: Function not found '%s'" % identifier_name)
			else:
				for tree in t.getKids():
					if tree is not t.getKid(1):
						self.traverse(tree)
			return [identifier_name, identifier_type, identifier_key]
		#################################
		#   check function is declared twice?
		#       declrTree kid:
		#           *typeTree
		#           *idTree
		#           *funcHead
		#           *block
		#################################
		elif isinstance(t, funcDeclTree):
			identifier_name, identifier_type, identifier_key = self.traverse(t.getKid(2))

			if identifier_name in self.identifier_function:
				for key in self.identifier_function[identifier_name]:
					if self.symbolTable.compare_scope(identifier_key, key):
						raise Exception("Error: Function '%s' is declared twice." %identifier_name)
				self.identifier_function[identifier_name].append(identifier_key)
			else:
				self.identifier_function[identifier_name] = [identifier_key]

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
			identifier_name, identifier_type, identifier_key = self.traverse(t.getKid(2))

			if identifier_type is None:
				raise Exception("Error: Variable not found '%s'" % identifier_name)
			else:
				if identifier_name in self.identifier_variable:
					for key in self.identifier_variable[identifier_name]:
						if self.symbolTable.compare_scope(identifier_key, key):
							raise Exception("Error: Variable '%s' is declared twice." % identifier_name)
					self.identifier_variable[identifier_name].append(identifier_key)
				else:
					if identifier_type == 'var':
						_, identifier_type, _ = self.traverse(t.getKid(3))
						if identifier_type is None: 
							identifier_type = "void"
						t.getKid(1).setType(identifier_type)
					self.identifier_variable[identifier_name] = [identifier_key]

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
			_, identifier_type_left, _ = self.traverse(t.getKid(1))
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
			_, identifier_type_left, _ = self.traverse(t.getKid(1))
			_, identifier_type_right, _ = self.traverse(t.getKid(2))

			compareGroupLeft = self.__comparableTypes.get(identifier_type_left, -1)
			compareGroupRight = self.__comparableTypes.get(identifier_type_right, -1)

			if compareGroupLeft != compareGroupRight or compareGroupLeft == -1:
				raise Exception(f'Comparisons between `{identifier_type_left}` and `{identifier_type_right}` are unsupported')
			else:
				return [None, 'boolean', None]
		#################################
		#   check if addOPTree has type mismatched.
		#       addOPTree kid:
		#           *expr
		#           add_op
		#           *expr
		#################################
		elif isinstance(t, addOPTree):
			_, identifier_type_left, _ = self.traverse(t.getKid(1))
			_, identifier_type_right, _ = self.traverse(t.getKid(2))

			try:
				return [None, compare(identifier_type_left, identifier_type_right), None]
			except NotImplemented:
				raise Exception(f"Addition operations between `{identifier_type_left}` and `{identifier_type_right}` are unsupported")

		#################################
		#   check if multOPTree has type mismatched
		#       multOPTree kid:
		#           *expr
		#           mult_op
		#           *expr
		#################################
		elif isinstance(t, multOPTree):
			_, identifier_type_left, leftKey = self.traverse(t.getKid(1))
			_, identifier_type_right, _ = self.traverse(t.getKid(2))

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
				return [None, compare(identifier_type_left, identifier_type_right), None]
			except NotImplemented:
				raise Exception(f"Multiplication operations between `{identifier_type_left}` and `{identifier_type_right}` are unsupported.")

		#################################
		#################################
		#################################
		#################################
		elif isinstance(t, numberTree):
			value = t.getContent()
			if '.' in value:
				if 'f' in value:
					identifier_type = 'float'
				else:
					identifier_type = 'double'
			else:
				if 'l' in value:
					identifier_type = 'long'
				else:
					identifier_type = 'int'
			return [value, identifier_type, None]
		elif isinstance(t, stringTree):
			identifier_type = "string"
			return [t.getContent(), identifier_type, None]
		elif isinstance(t, idTree):
			identifier_name, identifier_type = self.symbolTable.get_declaration_data(t.getKey())
			return [identifier_name, identifier_type, t.getKey()]
		else:
			for tree in t.getKids():
				self.traverse(tree)
