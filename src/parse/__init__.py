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
    def match(self, kinds):
        if type(kinds) is not list: kinds = [kinds]
        doesMatch = False
        for kind in kinds:
            if self.checkToken(kind):
                doesMatch = True
                matchType = kind
                break
        if not doesMatch:
            self.abort("Expected " + kind +
                       ", got " + self.curToken.value)
        self.nextToken()
        return matchType

    # Advances the current token.
    def nextToken(self):
        self.curToken = self.peekToken
        self.peekToken = next(self.tokens, token_names.EOF)
        # No need to worry about passing the EOF, lexer handles that.

    def abort(self, message):
        sys.exit("Error. " + message)

    def program(self):
        t = programTree()
        # match(token_names.KEYWORDS_ATTRIBUTE['public'])
        self.match(token_names.KEYWORDS_TYPE['class'])
        self.match(token_names.IDENTIFIER)
        t.addKid(self.block())
        return t

    def block(self):
        self.match(token_names.SEPARATORS['{'])
        t = blockTree()
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
        self.match(token_names.SEPARATORS['}'])
        return t

    def decl(self):
        typ, name = self.typ(), self.name()
        if self.checkToken(token_names.SEPARATORS['(']):
            t = funcDeclTree().addKid(typ).addKid(name)
            t.addKid(self.funcHead())
            t.addKid(self.block())
            return t
        if self.checkToken(token_names.OPERATORS['=']):
            t = declTreeWithAssign('Declaration with assignment').addKid(typ).addKid(name)
            t.addKid(self.expr())
            return t
        self.match(token_names.SEPARATORS[';'])
        t = declrTree().addKid(typ).addKid(name)
        return t
        
    def typ(self):
        t = typeTree()
        for key, types in token_names.KEYWORDS_TYPE:
            if self.checkToken(types):
                t.setLabel(key)
                self.nextToken()
                break
        if t.getLabel() == 'type':
            raise SyntaxError(f'Unrecognized type: {self.curToken.token_name}')
        return t

    def name(self):
        if self.checkToken(token_names.IDENTIFIER):
            t = idTree(self.curToken.value)
            self.nextToken()
            return t
        raise SyntaxError()

    def funcHead(self):
        self.match(token_names.SEPARATORS['('])
        t = funcHeadTree()
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
            self.nextToken()
            t.addKid(self.expr(), True)
            t.addKid(self.block())
            if self.checkToken(token_names.KEYWORDS['else']):
                self.nextToken()
                t.addKid(self.block())
            return t
        
        if self.checkToken(token_names.KEYWORDS['while']):
            t = whileTree()
            self.nextToken()
            t.addKid(self.expr(), True)
            t.addKid(self.block())
            return t

        if self.checkToken(token_names.KEYWORDS['return']):
            t = returnTree()
            self.nextToken()
            t.addKid(self.expr())
            return t

        if self.checkToken(token_names.SEPARATORS['{']):
            return self.block()

        assignOPs = [token_names.OPERATORS['='],
                     token_names.OPERATORS['+='], 
                     token_names.OPERATORS['-='], 
                     token_names.OPERATORS['*='], 
                     token_names.OPERATORS['/='], 
                     token_names.OPERATORS['%=']]
        kid = self.name()
        t = assignTree(self.match(assignOPs)).addKid(kid)
        t.addKid(self.expr())
        return t

    def expr(self, requireBracket=False):
        if requireBracket or self.checkToken(token_names.SEPARATORS['(']):
            self.match(token_names.SEPARATORS['('])
            requireBracket = True
        
        kid = self.simpleExpr()
        t = self.formRelationTree()
        if t is None:
            return kid

        t.addKid(kid)
        t.addKid(self.simpleExpr())
        return t

    def simpleExpr(self):
        addOPs = [token_names.OPERATORS['+'],
                     token_names.OPERATORS['-'],
                     token_names.OPERATORS['|']]

        kid = self.term()
        t = self.formAddOpTree()
        while t is not None:
            t.addKid(kid)
            t.addKid(self.term())
            kid = t
            t = self.formAddOpTree()
        return kid


    def formRelationTree(self):
        pass

    def formAddOpTree(self):
        pass

    def term(self):
        pass
