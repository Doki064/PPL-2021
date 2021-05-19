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
        return kind == self.curToken.getKind()

    # Return true if the next token matches.
    def checkPeek(self, kind):
        return kind == self.peekToken.getKind()

    # Try to match current token. If not, error. Advances the current token.
    def match(self, kind):
        if not self.checkToken(kind):
            self.abort("Expected " + kind.name +
                       ", got " + self.curToken.kind.name)
        self.nextToken()

    # Advances the current token.
    def nextToken(self):
        self.curToken = self.peekToken
        self.peekToken = next(self.tokens)
        # No need to worry about passing the EOF, lexer handles that.

    def abort(self, message):
        sys.exit("Error. " + message)

    def program(self):
        t = AST()
        match(token_names.keywords['public'])
        match(token_names.keywords['class'])
        match(token_names.IDENTIFIER)
        t.addKid(self.block())
        return t

    def block(self):
        match(token_names.separators['{'])
        t = AST()
        
