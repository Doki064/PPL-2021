"""This is the module to generate the symbol table.

This module would generate a symbol table from a collection of tokens.

Example:
    >>> from lex import Lexer
    >>> from symbol_table import SymbolTable
    >>>
    >>> lexer = Lexer(character_stream)
    >>> st = SymbolTable(lexer=lexer)
"""

__all__ = ["SymbolTable"]

from collections import UserDict as _UserDict
from typing import Tuple as _Tuple

try:
    from lex import Lexer as _Lexer
    from lex import LexerError as _LexerError
    from lex import Token as _Token
    from lex import token_names as _token_names
except ImportError:
    from src.lex import Lexer as _Lexer
    from src.lex import LexerError as _LexerError
    from src.lex import Token as _Token
    from src.lex import token_names as _token_names


class SymbolTable(_UserDict):
    """The symbol table.

    Attributes:
        current_token (_Token): The current token in the iteration.
        next_token (_Token): The next token in the iteration.
    """

    def __init__(self, lexer: _Lexer):
        """SymbolTable constructor.

        Takes lexer or tokens argument to get the collection of tokens. Prioritizes parser if both are provided.

        Args:
            lexer: The lexer for generating collections of token.

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

    def last(self):
        return next(reversed(self.data))

    def _generate(self):
        """Function for generating a symbol table."""
        scope_level = -1
        identifier_type = []
        identifier_attribute = []

        while self.current_token is not None:
            if self.current_token.check_token(_token_names.IDENTIFIER):
                identifier_key = identifier_position = self.current_token.key()
                identifier_name = self.current_token.value
                if self.next_token.check_token(_token_names.Separators("[")):
                    while True:
                        self._advance()
                        identifier_name += self.current_token.value
                        if (self.current_token.check_token(_token_names.Separators("]"))
                                and not self.next_token.check_token(_token_names.Separators("["))):
                            break

                if self.next_token.check_token(_token_names.Separators("(")):
                    identifier_type.append("function")

                if scope_level == -1:
                    scope = "outer_scope"
                elif scope_level == 0:
                    scope = "class_scope"
                elif scope_level >= 1:
                    scope = f"inner_scope_{scope_level}"
                else:
                    raise _LexerError(self.current_token.position, "Out of scope!")

                if not identifier_type:
                    try:
                        # A valid key must fulfill all the criteria below:
                        #   has the same identifier name,
                        #   its identifier type cannot be NoneType,
                        #   has the same or larger scope as the current identifier,
                        #   is the most recent key.
                        # If there is a valid key, pass it as the identifier_position for the current identifier.
                        latest_valid_key = next(key for key, value in reversed(self.data.items())
                                                if (value["identifier_name"] == identifier_name
                                                    and value["identifier_type"]
                                                    and value["identifier_scope"][1] <= scope_level))
                    except StopIteration:
                        pass
                    else:
                        identifier_position = latest_valid_key

                self[identifier_key] = {
                    "identifier_position": identifier_position,
                    "identifier_name": identifier_name,
                    "identifier_type": tuple(identifier_type),
                    "identifier_attribute": tuple(identifier_attribute),
                    "identifier_scope": (scope, scope_level),
                }
                identifier_type.clear()
                identifier_attribute.clear()

            elif self.current_token.check_token(_token_names.KeywordsType.names()):
                if self.next_token.check_token(_token_names.Separators("[")):
                    id_type = self.current_token.value
                    while True:
                        self._advance()
                        id_type += self.current_token.value
                        if (self.current_token.check_token(_token_names.Separators("]"))
                                and not self.next_token.check_token(_token_names.Separators("["))):
                            break
                    identifier_type.append(id_type)
                elif self.next_token.check_token(_token_names.IDENTIFIER):
                    identifier_type.append(self.current_token.value)

            elif self.current_token.check_token(_token_names.KeywordsAttribute.names()):
                if (self.next_token.check_token(_token_names.KeywordsAttribute.names())
                        or self.next_token.check_token(_token_names.KeywordsType.names())):
                    identifier_attribute.append(self.current_token.value)

            elif (self.current_token.check_token(_token_names.Separators("{"))
                  or self.current_token.check_token(_token_names.Separators("("))):
                scope_level += 1

            elif (self.current_token.check_token(_token_names.Separators("}"))
                  or self.current_token.check_token(_token_names.Separators(")"))):
                scope_level -= 1

            self._advance()

    def get_declaration_data(self, key):
        name = self.get_identifier_name(key)
        type = self.get_identifier_type(self.get_identifier_position(key))
        return name, type

    def get_identifier_position(self, identifier_key) -> int:
        """Gets the declared location of the given identifier key.

        Args:
            identifier_key (int): The dictionary key of the identifier.

        Returns:
            The value of identifier_position attribute of the identifier.
        """
        return self.get(identifier_key)["identifier_position"]

    def get_identifier_name(self, identifier_key) -> str:
        """Gets the name of the given identifier key.

        Args:
            identifier_key (int): The dictionary key of the identifier.

        Returns:
            The value of identifier_name attribute of the identifier.
        """
        return self.get(identifier_key)["identifier_name"]

    def get_identifier_type(self, identifier_key) -> _Tuple[str, ...]:
        """Gets the type of the given identifier key.

        Args:
            identifier_key (int): The dictionary key of the identifier.

        Returns:
            The tuple value of identifier_type attribute of the identifier.

        """
        return self.get(identifier_key)["identifier_type"]

    def get_identifier_attribute(self, identifier_key) -> _Tuple[str, ...]:
        """Gets the attributes of the given identifier key.

        Args:
            identifier_key (int): The dictionary key of the identifier.

        Returns:
            The value of identifier_attribute attribute of the identifier.
        """
        return self.get(identifier_key)["identifier_attribute"]

    def get_identifier_scope(self, identifier_key) -> _Tuple[str, int]:
        """Gets the scope of the given identifier key.

        Args:
            identifier_key (int): The dictionary key of the identifier.

        Returns:
            The value of identifier_scope attribute of the identifier,
                which is a tuple of scope name and scope level.

        Example:
            >>> st = SymbolTable(lexer=lexer)
            >>> scope = st.get_identifier_scope(12)
            >>> scope
            ("class_scope", 0)
        """
        return self.get(identifier_key)["identifier_scope"]
