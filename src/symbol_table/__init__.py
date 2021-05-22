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
from typing import Union as _Union

try:
    from lex import Lexer as _Lexer
    from lex import LexerError as _LexerError
    from lex import Token as _Token
    import mapper as _mapper
    import mapper.code_mapper as _code_mapper
except ImportError:
    from src.lex import Lexer as _Lexer
    from src.lex import LexerError as _LexerError
    from src.lex import Token as _Token
    import src.mapper as _mapper
    import src.mapper.code_mapper as _code_mapper


class SymbolTable(_UserDict):
    """The symbol table."""

    def __init__(self, lexer: _Lexer):
        """SymbolTable constructor.

        Takes lexer or tokens argument to get the collection of tokens. Prioritizes parser if both are provided.

        Args:
            lexer: The lexer for generating collections of token.
        """
        super().__init__()
        self.__tokens = lexer.tokens()
        self.__current_token = None
        self.__next_token = None
        self._advance()
        self._advance()
        self._generate()

    def _advance(self):
        """Advances the token collection."""
        self.__current_token = self.__next_token
        self.__next_token = next(self.__tokens, None)

    def _generate(self):
        """Function for generating a symbol table."""
        scope_level = -1
        scope_label = 0
        identifier_type = None
        identifier_attribute = []

        while self.__current_token is not None:
            if self.__current_token.check_token(_mapper.IDENTIFIER):
                identifier_key = identifier_position = self.__current_token.key()
                identifier_name = self.__current_token.value
                if self.__next_token.check_token(_mapper.Separators("[")):
                    while True:
                        self._advance()
                        identifier_name += self.__current_token.value
                        if (self.__current_token.check_token(_mapper.Separators("]"))
                                and not self.__next_token.check_token(_mapper.Separators("["))):
                            break

                if scope_level == -1:
                    scope = "outer_scope"
                elif scope_level == 0:
                    scope = "class_scope"
                elif scope_level >= 1:
                    scope = f"inner_scope_{scope_level}"
                else:
                    raise _LexerError(self.__current_token.position, "Out of scope!")

                if identifier_type is None:
                    try:
                        # A valid key must fulfill all the criteria below:
                        #   has the same identifier name,
                        #   its identifier type cannot be NoneType,
                        #   has the same or larger scope as the current identifier,
                        #   is the most recent key.
                        # If there is a valid key, pass it as the identifier_position for the current identifier.
                        latest_valid_key = next(key for key, value in reversed(self.data.items())
                                                if (value["identifier_name"] == identifier_name
                                                    and value["identifier_type"] is not None
                                                    and value["identifier_scope"][1] <= scope_level))
                    except StopIteration:
                        pass
                    else:
                        identifier_position = latest_valid_key

                    if identifier_name in _code_mapper.Double_Java or identifier_name == "scanner.nextDouble":
                        identifier_type = "double"
                    elif identifier_name in _code_mapper.Float_Java:
                        identifier_type = "float"
                    elif identifier_name in _code_mapper.Long_Java:
                        identifier_type = "long"
                    elif identifier_name in _code_mapper.Int_Java:
                        identifier_type = "int"
                    elif identifier_name in _code_mapper.Short_Java:
                        identifier_type = "short"
                    elif identifier_name in _code_mapper.Byte_Java:
                        identifier_type = "byte"
                    elif identifier_name in _code_mapper.String_Java:
                        identifier_type = "String"

                self[identifier_key] = {
                    "identifier_position": identifier_position,
                    "identifier_name": identifier_name,
                    "identifier_type": identifier_type,
                    "identifier_attribute": tuple(identifier_attribute),
                    "identifier_scope": (scope, scope_level),
                    "scope_label": scope_label,
                }
                identifier_type = None
                identifier_attribute.clear()

            elif self.__current_token.check_token(_mapper.KeywordsType.names()):
                position = self.__current_token.position
                identifier_type = self.__current_token.value
                while self.__next_token.check_token(_mapper.KeywordsType.names()):
                    self._advance()
                    identifier_type += " " + self.__current_token.value
                if self.__next_token.check_token(_mapper.Separators("[")):
                    while True:
                        self._advance()
                        identifier_type += self.__current_token.value
                        if (self.__current_token.check_token(_mapper.Separators("]"))
                                and not self.__next_token.check_token(_mapper.Separators("["))):
                            break
                if not self.__next_token.check_token(_mapper.IDENTIFIER):
                    raise SyntaxError(
                        f"Invalid data type `{identifier_type + ' ' + self.__next_token.value}` at line {position}")

            elif self.__current_token.check_token(_mapper.KeywordsAttribute.names()):
                if (self.__next_token.check_token(_mapper.KeywordsAttribute.names())
                        or self.__next_token.check_token(_mapper.KeywordsType.names())):
                    identifier_attribute.append(self.__current_token.value)

            elif (self.__current_token.check_token(_mapper.Separators("{"))
                  or self.__current_token.check_token(_mapper.Separators("("))):
                scope_level += 1
                scope_label += 1

            elif (self.__current_token.check_token(_mapper.Separators("}"))
                  or self.__current_token.check_token(_mapper.Separators(")"))):
                scope_level -= 1

            self._advance()

    def get_declaration_data(self, key):
        """Returns the declaration type of the identifier with the given key.

        Args:
            key (int): The dictionary key of the identifier.

        Returns:
            Returns the declaration type of the identifier with the given key.
                None if the identifier is not declared.
        """
        name = self.get_identifier_name(key)
        typ = self.get_identifier_type(self.get_identifier_position(key))
        return name, typ

    def compare_scope(self, key_a, key_b) -> int:
        """Returns True if the same scope.

        Args:
            key_a (int): The first key.
            key_b (int): The second key.

        Returns:
            Returns positive if scope A > scope B, 0 if equal, and negative if scope A < scope B.
        """
        a_scope = self.get(key_a)["scope_label"]
        b_scope = self.get(key_b)["scope_label"]
        return b_scope - a_scope

    def get_identifier_position(self, identifier_key) -> int:
        """Gets the declared position of the identifier with the given key.

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

    def get_identifier_type(self, identifier_key) -> _Union[str, None]:
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
