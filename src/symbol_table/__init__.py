"""This is the module to generate the symbol table.

    This module would generate a symbol table from a collection of tokens.

    Example:
        >>> from lex import Lexer
        >>> from symbol_table import SymbolTable
        >>> lexer = Lexer(character_stream)
        >>> st = SymbolTable(lexer=lexer)
        >>> print(st) # Recommend to use pprint: pprint.pprint(st)
"""

from collections import OrderedDict

try:
    from lex import *
except Exception:
    from src.lex import *


class SymbolTable(OrderedDict):
    """The symbol table.

        Attributes:
            tokens (Iterable[Token]): The iterator over the collection tokens.
            current_token (Token): The current token in the iteration.
            next_token (Token): The next token in the iteration.
    """

    def __init__(self, lexer=None, tokens=None):
        """SymbolTable constructor.

            Takes lexer or tokens argument to get the collection of tokens. Prioritizes lexer if both are provided.

            Args:
                lexer (Lexer): The lexer for generating collections of token. Defaults to None.
                tokens (Iterable[Token]): The iterator over the collection tokens. Defaults to None.

        """

        super().__init__()
        if lexer is not None:
            self.tokens = lexer.tokens()
        elif tokens is not None:
            self.tokens = tokens
        else:
            raise TypeError("__init__() needs at least 1 argument: 'lexer' or 'tokens'.")
        self.current_token = None
        self.next_token = None
        self._advance()
        self._advance()
        self._generate()

    def _advance(self):
        """Advances the token collection."""
        self.current_token = self.next_token
        self.next_token = next(self.tokens, None)

    def _check_token(self, *args):
        if len(args) == 1:
            if isinstance(args[0], str) or isinstance(args[0], token_names.Enum):
                return self.current_token.token_name == args[0]
            elif isinstance(args[0], Iterable):
                return self.current_token.token_name in args[0]
        raise TypeError("_check_token() taking 1 argument, type: str, Enum or Iterable object")

    def _generate(self):
        """Function for generating a symbol table."""
        scope_level = -1
        identifier_type = None
        attributes = []

        while self.current_token is not None:
            if self._check_token(token_names.IDENTIFIER):
                identifier_key = identifier_position = self.current_token.position
                identifier_name = self.current_token.value
                if self._check_token(token_names.Separators("[")):
                    while True:
                        self._advance()
                        identifier_name += self.current_token.value
                        if (self._check_token(token_names.Separators("]"))
                                and not self._check_token(token_names.Separators("["))):
                            break
                if scope_level == -1:
                    scope = "outer_scope"
                elif scope_level == 0:
                    scope = "class_scope"
                elif scope_level >= 1:
                    scope = f"inner_scope_{scope_level}"
                else:
                    raise LexerError(self.current_token.left_position, "Out of scope!")

                if identifier_type is None:
                    try:
                        # A valid key must fulfill all the criteria below:
                        #   has the same identifier name,
                        #   its identifier type cannot be NoneType,
                        #   has the same or larger scope as the current identifier,
                        #   is the most recent key.
                        # If there is a valid key, pass it as the identifier_position for the current identifier.
                        latest_valid_key = next(key for key, value in reversed(self.items())
                                                if (value["identifier_name"] == identifier_name
                                                    and value["identifier_type"] is not None
                                                    and value["scope"][1] <= scope_level))
                    except StopIteration:
                        pass
                    else:
                        identifier_position = latest_valid_key

                self[identifier_key] = {
                    "identifier_position": identifier_position,
                    "identifier_name": identifier_name,
                    "identifier_type": identifier_type,
                    "attributes": tuple(attributes),
                    "scope": (scope, scope_level),
                }
                identifier_type = None
                attributes.clear()

            elif self._check_token(token_names.KeywordsType.names()):
                if self._check_token(token_names.Separators("[")):
                    identifier_type = self.current_token.value
                    while True:
                        self._advance()
                        identifier_type += self.current_token.value
                        if (self._check_token(token_names.Separators("]"))
                                and not self._check_token(token_names.Separators("["))):
                            break
                elif self._check_token(token_names.IDENTIFIER):
                    identifier_type = self.current_token.value

            elif self._check_token(token_names.KeywordsAttribute.names()):
                if (self._check_token(token_names.KeywordsAttribute.names())
                        or self._check_token(token_names.KeywordsType.names())):
                    attributes.append(self.current_token.value)

            elif (self._check_token(token_names.Separators("{"))
                  or self._check_token(token_names.Separators("("))):
                scope_level += 1

            elif (self._check_token(token_names.Separators("}"))
                  or self._check_token(token_names.Separators(")"))):
                scope_level -= 1

            self._advance()
