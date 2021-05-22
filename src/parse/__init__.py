__all__ = ["Parser"]

from sys import exit

try:
    from ast import *
    from lex import token_names as _token_names
except ImportError:
    from src.ast import *
    from src.lex import token_names as _token_names

# Parser object keeps track of current token and checks if the code matches the grammar.


class Parser:
    assignOPs = [_token_names.OPERATORS['='],
                 _token_names.OPERATORS['+='],
                 _token_names.OPERATORS['-='],
                 _token_names.OPERATORS['*='],
                 _token_names.OPERATORS['/='],
                 _token_names.OPERATORS['%=']]

    relOPs = [_token_names.OPERATORS['<'],
              _token_names.OPERATORS['<='],
              _token_names.OPERATORS['>'],
              _token_names.OPERATORS['>='],
              _token_names.OPERATORS['=='],
              _token_names.OPERATORS['!=']]

    addOPs = [_token_names.OPERATORS['+'],
              _token_names.OPERATORS['-'],
              _token_names.OPERATORS['|']]

    multOPs = [_token_names.OPERATORS['*'],
               _token_names.OPERATORS['/'],
               _token_names.OPERATORS['&']]

    def __init__(self, lexer):
        self.tokens = lexer.tokens()
        self.curToken = None
        self.peekToken = None
        self.nextToken()
        self.nextToken()  # Call this twice to initialize current and peek.

    # Return true if the current token matches.
    def checkToken(self, kind):
        return kind == self.curToken.token_name

    # Return true if the next token matches.
    def checkPeek(self, kind):
        return kind == self.peekToken.token_name

    # Try to match current token. If not, error. Advances the current token.
    def match(self, kinds):
        if type(kinds) is not list:
            kinds = [kinds]
        doesMatch = False
        for kind in kinds:
            if self.checkToken(kind):
                doesMatch = True
                matchType = kind
                break
        if not doesMatch:
            self.abort(
                f'Expected {_token_names.get_value_by_name(kind)}, got {self.curToken.value}, at line {self.curToken.position}')
        self.nextToken()
        return matchType

    # Advances the current token.
    def nextToken(self):
        self.curToken = self.peekToken
        self.peekToken = next(self.tokens, _token_names.EOF)
        # No need to worry about passing the EOF, lexer handles that.

    @staticmethod
    def abort(message):
        exit("Error. " + message)

#             HELPER FUNCTION DECLARATIONS END HERE                   #
# --------------------------------------------------------------------#
#               PARSING LOGIC STARTS FROM HERE                        #

    def program(self):
        t = programTree()
        # match(_token_names.KEYWORDS_ATTRIBUTE['public'])
        self.match(_token_names.KEYWORDS_TYPE['class'])
        self.match(_token_names.IDENTIFIER)
        t.addKid(self.block())
        return t

    def block(self):
        self.match(_token_names.SEPARATORS['{'])
        t = blockTree()
        while True:
            try:
                t.addKid(self.statement())
            except SyntaxError:
                break
        self.match(_token_names.SEPARATORS['}'])
        return t

    def decl(self, requireSemiColon=True):
        typ, name = self.typ(), self.name()
        if self.checkToken(_token_names.SEPARATORS['(']):
            t = funcDeclTree().addKid(typ).addKid(name)
            t.addKid(self.funcHead())
            t.addKid(self.block())
            return t
        if self.checkToken(_token_names.OPERATORS['=']) and requireSemiColon:
            self.nextToken()
            t = declrTree().addKid(typ).addKid(name).addKid(self.expr())
            self.match(_token_names.SEPARATORS[';'])
            t.addKid(endTree())
            return t
        t = declrTree().addKid(typ).addKid(name)
        if requireSemiColon:
            self.match(_token_names.SEPARATORS[';'])
            t.addKid(endTree())
        return t

    def typ(self):
        t = typeTree()
        for key in _token_names.KEYWORDS_TYPE:
            typ = _token_names.KEYWORDS_TYPE[key]
            if self.checkToken(typ):
                t.setType(key)
                self.nextToken()
                break

        if t.getType == 'Type':
            raise SyntaxError(f'Unrecognized type: {_token_names.get_value_by_name(self.curToken.token_name)}')

        if self.checkToken(_token_names.SEPARATORS['[']):
            self.nextToken()
            self.match(_token_names.SEPARATORS[']'])
            t.setArray()
        return t

    def name(self):
        if self.checkToken(_token_names.IDENTIFIER):
            t = idTree(self.curToken.value, self.curToken.key())
            self.nextToken()
            return t
        raise SyntaxError(
            f'Expected: {_token_names.IDENTIFIER}, got {_token_names.get_value_by_name(self.curToken.token_name)}, at line {self.curToken.position}')

    def funcHead(self):
        self.match(_token_names.SEPARATORS['('])
        t = funcHeadTree()
        if not self.checkToken(_token_names.SEPARATORS[')']):
            while True:
                t.addKid(self.decl(requireSemiColon=False))
                if self.checkToken(_token_names.SEPARATORS[',']):
                    self.nextToken()
                else:
                    break
        self.match(_token_names.SEPARATORS[')'])
        return t

    def statement(self):
        if self.curToken.token_name in _token_names.KEYWORDS_TYPE.values():
            return self.decl()
        if self.checkToken(_token_names.KEYWORDS['if']):
            t = ifTree()
            self.nextToken()
            t.addKid(self.expr(True))
            t.addKid(self.block())
            if self.checkToken(_token_names.KEYWORDS['else']):
                self.nextToken()
                t.addKid(self.block())
            return t

        if self.checkToken(_token_names.KEYWORDS['while']):
            t = whileTree()
            self.nextToken()
            t.addKid(self.expr(True))
            t.addKid(self.block())
            return t

        if self.checkToken(_token_names.KEYWORDS['return']):
            t = returnTree()
            self.nextToken()
            t.addKid(self.expr())
            self.match(_token_names.SEPARATORS[';'])
            t.addKid(endTree())
            return t

        if self.checkToken(_token_names.SEPARATORS['{']):
            return self.block()

        kid = self.name()

        if self.checkToken(_token_names.SEPARATORS['(']):
            self.nextToken()
            t = callTree().addKid(kid)
            if not self.checkToken(_token_names.SEPARATORS[')']):
                while True:
                    t.addKid(self.expr())
                    if self.checkToken(_token_names.SEPARATORS[',']):
                        self.nextToken()
                    else:
                        break
            self.match(_token_names.SEPARATORS[')'])
            self.match(_token_names.SEPARATORS[';'])
            t.addKid(endTree())
            return t

        t = assignTree(self.match(Parser.assignOPs)).addKid(kid)
        t.addKid(self.expr())
        self.match(_token_names.SEPARATORS[';'])
        t.addKid(endTree())
        return t

    def expr(self, requireBracket=False):
        if requireBracket:
            self.match(_token_names.SEPARATORS['('])
            requireBracket = True

        kid = self.simpleExpr()
        t = self.formRelationTree()
        if t is None:
            if requireBracket:
                self.match(_token_names.SEPARATORS[')'])
            return kid

        t.addKid(kid)
        t.addKid(self.simpleExpr())

        if requireBracket:
            self.match(_token_names.SEPARATORS[')'])
        return t

    def simpleExpr(self):
        kid = self.term()
        t = self.formAddOpTree()
        while t is not None:
            t.addKid(kid)
            t.addKid(self.term())
            kid = t
            t = self.formAddOpTree()
        return kid

    def term(self):
        kid = self.factor()
        t = self.formMultOpTree()
        while t is not None:
            t.addKid(kid)
            t.addKid(self.factor())
            kid = t
            t = self.formMultOpTree()
        return kid

    def factor(self):
        if self.checkToken(_token_names.SEPARATORS['(']):
            self.nextToken()
            t = self.expr()
            self.match(_token_names.SEPARATORS[')'])
            return t

        if self.checkToken(_token_names.NUMBER):
            t = numberTree(self.curToken.value)
            self.nextToken()
            return t

        if self.checkToken(_token_names.STRING):
            t = stringTree(self.curToken.value)
            self.nextToken()
            return t

        t = self.name()
        if not self.checkToken(_token_names.SEPARATORS['(']):
            return t

        self.nextToken()
        t = callTree().addKid(t)
        if not self.checkToken(_token_names.SEPARATORS[')']):
            while True:
                t.addKid(self.expr())
                if self.checkToken(_token_names.SEPARATORS[',']):
                    self.nextToken()
                else:
                    break
        self.match(_token_names.SEPARATORS[')'])
        return t

    def formRelationTree(self):
        if self.curToken.token_name in Parser.relOPs:
            t = relOPTree(self.curToken.token_name)
            self.nextToken()
            return t
        else:
            return None

    def formAddOpTree(self):
        if self.curToken.token_name in Parser.addOPs:
            t = addOPTree(self.curToken.token_name)
            self.nextToken()
            return t
        else:
            return None

    def formMultOpTree(self):
        if self.curToken.token_name in Parser.multOPs:
            t = multOPTree(self.curToken.token_name)
            self.nextToken()
            return t
        else:
            return None
