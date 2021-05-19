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
                identifier_position = self.current_token.left_position
                identifier_name = self.current_token.value
                if self.next_token.token_name == token_names.SEPARATORS.get("["):
                    while True:
                        self._advance()
                        identifier_name += self.current_token.value
                        if (self.current_token.token_name == token_names.SEPARATORS.get("]")
                                and self.next_token.token_name != token_names.SEPARATORS.get("[")):
                            break
                if scope_level == -1:
                    scope = "outer_scope"
                elif scope_level == 0:
                    scope = "class_scope"
                elif scope_level >= 1:
                    scope = f"inner_scope_{scope_level}"
                else:
                    raise LexerError(self.current_token.position, "Out of scope!")

                for value in self.values():
                    if value["identifier_name"] == identifier_name:
                        if identifier_type is None:
                            break
                else:
                    self[identifier_position] = {
                        "identifier_position": identifier_position,
                        "identifier_name": identifier_name,
                        "identifier_type": identifier_type,
                        "attributes": tuple(attributes),
                        "scope": scope,
                    }

                identifier_type = None
                attributes.clear()

            elif self.current_token.token_name in token_names.KEYWORDS_TYPE.values():
                if self.next_token.token_name == token_names.SEPARATORS.get("["):
                    identifier_type = self.current_token.value
                    while True:
                        self._advance()
                        identifier_type += self.current_token.value
                        if (self.current_token.token_name == token_names.SEPARATORS.get("]")
                                and self.next_token.token_name != token_names.SEPARATORS.get("[")):
                            break
                elif self.next_token.token_name == token_names.IDENTIFIER:
                    identifier_type = self.current_token.value

            elif self.current_token.token_name in token_names.KEYWORDS_ATTRIBUTE.values():
                if (self.next_token.token_name in token_names.KEYWORDS_ATTRIBUTE.values()
                        or self.next_token.token_name in token_names.KEYWORDS_TYPE.values()):
                    attributes.append(self.current_token.value)

            elif (self.current_token.token_name == token_names.SEPARATORS.get("{")
                  or self.current_token.token_name == token_names.SEPARATORS.get("(")):
                scope_level += 1

            elif (self.current_token.token_name == token_names.SEPARATORS.get("}")
                  or self.current_token.token_name == token_names.SEPARATORS.get(")")):
                scope_level -= 1

            self._advance()
