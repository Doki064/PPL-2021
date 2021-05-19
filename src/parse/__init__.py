import sys

from lex import *
from ast import *

# Parser object keeps track of current token and checks if the code matches the grammar.
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer

        self.tokens = lexer.tokens()

        self.curToken = None
        self.peekToken = None
        self.nextToken()
        self.nextToken()    # Call this twice to initialize current and peek.

    # Return true if the current token matches.
    def checkToken(self, kind):
        return kind == self.curToken.token_name

    # Return true if the next token matches.
    def checkPeek(self, kind):
        return kind == self.peekToken.token_name

    # Try to match current token. If not, error. Advances the current token.
    def match(self, kind):
        if not self.checkToken(kind):
            self.abort("Expected " + kind +
                       ", got " + self.curToken.value)
        self.nextToken()

    # Advances the current token.
    def nextToken(self):
        self.curToken = self.peekToken
        self.peekToken = next(self.tokens, token_names.EOF)
        # No need to worry about passing the EOF, lexer handles that.

    def abort(self, message):
        sys.exit("Error. " + message)

    def program(self):
        t = programTree('Program/Class')
        # match(token_names.KEYWORDS_ATTRIBUTE['public'])
        match(token_names.KEYWORDS_TYPE['class'])
        match(token_names.IDENTIFIER)
        t.addKid(self.block())
        return t

    def block(self):
        match(token_names.SEPARATORS['{'])
        t = blockTree('Code block')
        while True:
            try:
                t.addKid(self.decl())
            except SyntaxError:
                break
        while True:
            try:
                t.addKid(self.statement())
            except SyntaxError:
                break
        match(token_names.SEPARATORS['}'])
        return t

    def decl(self):
        typ, name = self.typ(), self.name()
        if self.checkToken(token_names.SEPARATORS['(']):
            t = funcDeclTree('Function').addKid(typ).addKid(name)
            t.addKid(self.funcHead())
            t.addKid(self.block())
            return t
        if self.checkToken(token_names.OPERATORS['=']):
            t = declTreeWithAssign('Declaration with assignment').addKid(typ).addKid(name)
            t.addKid(self.expr())
            return t
        self.match(token_names.SEPARATORS[';'])
        t = declrTree('Declaration').addKid(typ).addKid(name)
        return t
        
    def typ(self):
        t = typeTree('')
        for key, types in token_names.KEYWORDS_TYPE:
            if self.checkToken(types):
                t.setLabel(key)
                self.nextToken()
                break
        if t.getLabel() == '':
            raise SyntaxError(f'Unrecognized type: {self.curToken.token_name}')
        return t

    def name(self):
        if self.checkToken(token_names.IDENTIFIER):
            t = idTree('id', self.curToken.value)
            self.nextToken()
            return t
        raise SyntaxError()

    def funcHead(self):
        self.match(token_names.SEPARATORS['('])
        t = funcHeadTree('Function Header')
        if not self.checkToken(token_names.SEPARATORS[')']):
            while True:
                t.addKid(self.decl())
                if self.checkToken(token_names.SEPARATORS[',']):
                    self.nextToken()
                else:
                    break
        match(token_names.SEPARATORS[')'])
        return t

    def statement(self):
        if self.checkToken(token_names.KEYWORDS['if']):
            t = ifTree()

    def expr(self):
        pass