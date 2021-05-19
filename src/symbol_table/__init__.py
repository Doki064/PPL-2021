from collections import OrderedDict

from src.lex import *


class SymbolTable(OrderedDict):
    """The symbol table.

        Attributes:
            tokens (Iterator[Token]): The iterator over the collection tokens.
            current_token (Token): The current token in the iteration.
            next_token (Token): The next token in the iteration.
    """

    def __init__(self, lexer):
        """SymbolTable constructor.

            Args:
                lexer (Lexer): The lexer for generating collections of token.
        """

        super().__init__()
        self.tokens = lexer.tokens()
        self.current_token = None
        self.next_token = None
        self._advance()
        self._advance()
        self._generate()

    def _advance(self):
        """Advances the token collection."""
        self.current_token = self.next_token
        self.next_token = next(self.tokens, None)

    def _generate(self):
        """Function for generating a symbol table."""
        scope_level = -1
        identifier_type = None
        attributes = []

        while self.current_token is not None:
            if self.current_token.token_name == token_names.IDENTIFIER:
                identifier_key = identifier_position = self.current_token.left_position
                identifier_name = self.current_token.value
                if self.next_token.token_name == token_names.Separators("[").name:
                    while True:
                        self._advance()
                        identifier_name += self.current_token.value
                        if (self.current_token.token_name == token_names.Separators("]").name
                                and self.next_token.token_name != token_names.Separators("[").name):
                            break
                if scope_level == -1:
                    scope = "outer_scope"
                elif scope_level == 0:
                    scope = "class_scope"
                elif scope_level >= 1:
                    scope = f"inner_scope_{scope_level}"
                else:
                    raise LexerError(self.current_token.left_position, "Out of scope!")

                for key, value in reversed(self.items()):
                    # all_keys = [key for key, value in self.items() if value["identifier_type"] is not None]
                    if identifier_type is None:
                        if (value["identifier_name"] == identifier_name
                                and value["identifier_type"] is not None
                                and value["scope"][1] <= scope_level):
                            identifier_position = key
                else:
                    self[identifier_key] = {
                        "identifier_position": identifier_position,
                        "identifier_name": identifier_name,
                        "identifier_type": identifier_type,
                        "attributes": tuple(attributes),
                        "scope": (scope, scope_level),
                    }
                identifier_type = None
                attributes.clear()

            elif self.current_token.token_name in token_names.KeywordsType.names():
                if self.next_token.token_name == token_names.Separators("[").name:
                    identifier_type = self.current_token.value
                    while True:
                        self._advance()
                        identifier_type += self.current_token.value
                        if (self.current_token.token_name == token_names.Separators("]").name
                                and self.next_token.token_name != token_names.Separators("[").name):
                            break
                elif self.next_token.token_name == token_names.IDENTIFIER:
                    identifier_type = self.current_token.value

            elif self.current_token.token_name in token_names.KeywordsAttribute.names():
                if (self.next_token.token_name in token_names.KeywordsAttribute.names()
                        or self.next_token.token_name in token_names.KeywordsType.names()):
                    attributes.append(self.current_token.value)

            elif (self.current_token.token_name == token_names.Separators("{").name
                  or self.current_token.token_name == token_names.Separators("(").name):
                scope_level += 1

            elif (self.current_token.token_name == token_names.Separators("}").name
                  or self.current_token.token_name == token_names.Separators(")").name):
                scope_level -= 1

            self._advance()
