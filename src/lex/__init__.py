"""This is the module containing all codes needed for the lexer.

This module would take the character stream and generate a collection of tokens.

Example:
    >>> from lex import Lexer
    >>>
    >>> with open(path_to_file, "r") as f:
    >>>     character_stream = f.read()
    >>> lexer = Lexer(character_stream)

    # Lexer has an Iterator to get tokens:

    >>> for token in lexer.tokens():
    >>>     print(token)
"""

__all__ = [
    "token_names",
    "Token",
    "LexerError",
    "Lexer",
]

from enum import Enum as _Enum
from typing import Iterator as _Iterator
from typing import Sequence as _Sequence

from lex import token_names as _token_names


class Token:
    """ A simple Token structure.

    Contains the token position, name and value.

    Attributes:
        position (int): The position of the token.
        token_name (str): The name of the token.
        value (str): The value of the token.
    """

    def __init__(self, start_position, end_position, token_name, value):
        """Token constructor.

        Args:
            start_position (int): The start position of the token.
            end_position (int): The end position of the token.
            token_name (str): The name of the token.
            value (str): The value of the token.
        """
        self.position = self._start_position = start_position
        self._end_position = end_position
        self.token_name = token_name
        self.value = value

    def check_token(self, *args) -> bool:
        """Check the token type whether it matches that of the passed argument.

        Args:
            *args: The function takes only one argument, which can be a string, an enum object, or a sequence object.

        Returns:
            True if matches, False otherwise.
                If the argument is a sequence, True if it contains this token type, False otherwise.

        Raises:
            TypeError: An error occurred when the argument is missing, or of incorrect types.
        """
        if len(args) == 1:
            if isinstance(args[0], str):
                return self.token_name == args[0]
            elif isinstance(args[0], _Enum):
                return self.token_name == args[0].name
            elif isinstance(args[0], _Sequence):
                return self.token_name in args[0]
        raise TypeError("_check_token() taking 1 argument, type: str, Enum or Sequence")

    def __str__(self):
        return f"{self._start_position}\t {self._end_position}\t {self.token_name}\t {self.value}"

    def __hash__(self):
        return hash((self.position, self.token_name, self.value))

    def __eq__(self, other):
        if isinstance(other, Token):
            return self.position == other.position and self.token_name == other.token_name and self.value == other.value
        return NotImplemented


class LexerError(Exception):
    """Lexer exception.

    Attributes:
        position (int): The position in the stream where the error occurred.
        message (str): Human readable description of the error.
    """

    def __init__(self, position, message: str = None):
        """LexerError constructor.

        Args:
            position (int): The start position of the error.
            message: Human readable description of the error. Optional.
        """
        self.position = position
        self.message = f"Unknown token at position {self.position}" if message is None else message
        super().__init__(self.message)


class Lexer:
    """The lexer.

    Scans the file as stream and tokenize it.

    Attributes:
        stream (str): The data to work on.
        EOF (boolean): The flag to indicate end of file.
        current_position (int): The position in the stream currently.
        current_char (str): The current character.
    """

    def __init__(self, character_stream):
        """Lexer constructor.

        Args:
            character_stream (str): The character stream of the input file.
        """
        self.stream = character_stream
        self.EOF = False
        self.current_position = -1
        self.current_char = ""
        self._next_char()

    def _next_char(self):
        """Moves to the next character. Set `EOF` to True when end of file."""
        self.current_position += 1
        if self.current_position >= len(self.stream):
            self.current_char = "\0"
            self.EOF = True
        else:
            self.current_char = self.stream[self.current_position]

    def _peek(self):
        """Returns the lookahead character.

        Returns:
            str: The next character in the stream, null character "\0" if end of file.
        """
        if self.current_position + 1 >= len(self.stream):
            return "\0"
        return self.stream[self.current_position + 1]

    def _skip(self):
        """Skips whitespaces, newlines and comments.

        Raises:
            LexerError: An error occurred while getting tokens in the character stream.
        """
        if self.current_char == "/":
            last_position = self.current_position
            if self._peek() == "/":  # Single-line comment
                while self.current_char != "\n":
                    self._next_char()
            elif self._peek() == "*":  # Multiple-line comment
                while self.current_char != "*" or self._peek() != "/":
                    self._next_char()
                    if self.EOF:  # Check unclosed comment
                        raise LexerError(
                            last_position, f"Unclosed comment at position {last_position}")
                self._next_char()
                self._next_char()

        while self.current_char in [" ", "\t", "\r", "\n"]:
            self._next_char()

    def _get_token(self):
        """Returns the next token.

        Returns:
            Token: An token found in the stream.

        Raises:
            LexerError: An error occurred while getting tokens in the character stream.
        """
        self._skip()

        token = None
        # Checks single-quoted string.
        if self.current_char == "'":
            start_position = self.current_position
            while not (self.current_char != "\\" and self._peek() == "'"):
                self._next_char()
                if self.EOF:
                    raise LexerError(
                        start_position, f"EOL while scanning string literal at position {start_position}")
            self._next_char()
            token = Token(start_position, self.current_position,
                          _token_names.STRING, self.stream[start_position:self.current_position + 1])

        # Checks double-quoted string.
        elif self.current_char == '"':
            start_position = self.current_position
            while not (self.current_char != "\\" and self._peek() == '"'):
                self._next_char()
                if self.EOF:
                    raise LexerError(
                        start_position, f"EOL while scanning string literal at position {start_position}")
            self._next_char()
            token = Token(start_position, self.current_position,
                          _token_names.STRING, self.stream[start_position:self.current_position + 1])

        # Checks number begins with a digit.
        elif self.current_char.isdigit():
            start_position = self.current_position
            while self._peek().isdigit():
                self._next_char()
            if self._peek() == ".":
                self._next_char()
                while self._peek().isdigit():
                    self._next_char()
            if self._peek() in ["d", "D", "f", "F"]:
                self._next_char()
            token = Token(start_position, self.current_position,
                          _token_names.NUMBER, self.stream[start_position:self.current_position + 1])

        # Checks number begins with a dot.
        elif self.current_char == ".":
            if self._peek().isdigit():
                start_position = self.current_position
                while self._peek().isdigit():
                    self._next_char()
                if self._peek() in ["d", "D", "f", "F"]:
                    self._next_char()
                token = Token(start_position, self.current_position,
                              _token_names.NUMBER, self.stream[start_position:self.current_position + 1])
            else:
                token = Token(self.current_position, self.current_position,
                              _token_names.Separators(self.current_char).name, self.current_char)

        # Checks word begins with an alphabetic letter or an underscore.
        elif self.current_char.isalpha() or self.current_char == "_":
            start_position = self.current_position
            while True:
                if (self._peek() in [" ", "\t", "\r", "\n", "\0"]
                        or self._peek() in _token_names.SEPARATORS
                        or self._peek() in _token_names.OPERATORS):
                    break
                self._next_char()
            word = self.stream[start_position:self.current_position + 1]
            # Checks if word is a keyword.
            if word in _token_names.Keywords.values():
                token = Token(start_position, self.current_position,
                              _token_names.Keywords(word).name, word)
            elif word in _token_names.KeywordsType.values():
                token = Token(start_position, self.current_position,
                              _token_names.KeywordsType(word).name, word)
            elif word in _token_names.KeywordsAttribute.values():
                token = Token(start_position, self.current_position,
                              _token_names.KeywordsAttribute(word).name, word)
            # Otherwise put it as identifier.
            else:
                token = Token(start_position, self.current_position,
                              _token_names.IDENTIFIER, word)

        # Checks if is a separator.
        elif self.current_char in _token_names.Separators.values():
            token = Token(self.current_position, self.current_position,
                          _token_names.Separators(self.current_char).name, self.current_char)

        # Checks if is an operator.
        elif self.current_char in _token_names.Operators.values():
            last_position = self.current_position
            if self.current_char not in ["&", "|"] and self._peek() == "=":
                val = self.current_char + self._peek()
                self._next_char()
                token = Token(last_position, self.current_position,
                              _token_names.Operators(val).name, val)
            elif self.current_char == "+" and self._peek() == "+":
                val = self.current_char + self._peek()
                self._next_char()
                token = Token(last_position, self.current_position,
                              _token_names.Operators(val).name, val)
            elif self.current_char == "-" and self._peek() == "-":
                val = self.current_char + self._peek()
                self._next_char()
                token = Token(last_position, self.current_position,
                              _token_names.Operators(val).name, val)
            elif self.current_char == "&" and self._peek() == "&":
                val = self.current_char + self._peek()
                self._next_char()
                token = Token(last_position, self.current_position,
                              _token_names.Operators(val).name, val)
            elif self.current_char == "|" and self._peek() == "|":
                val = self.current_char + self._peek()
                self._next_char()
                token = Token(last_position, self.current_position,
                              _token_names.Operators(val).name, val)
            else:
                token = Token(self.current_position, self.current_position,
                              _token_names.Operators(self.current_char).name, self.current_char)

        # Checks if is EOF
        elif self.current_char == "\0":
            token = Token(self.current_position, self.current_position,
                          _token_names.EOF, self.current_char)

        # Raise error if is an unknown token.
        else:
            raise LexerError(self.current_position)

        self._next_char()
        return token

    def reset(self):
        """Resets the lexer to its initial state."""
        self.EOF = False
        self.current_position = -1
        self.current_char = ""
        self._next_char()

    def tokens(self, ignore=True) -> _Iterator[Token]:
        """ An generator to iterate over all of the tokens found in the character stream.

        Args:
            ignore (bool): If True, ignore all of the unsupported tokens.

        Yields:
            Token: A token object.

        Raises:
            LexerError: An error occurred while getting tokens in the character stream.
        """
        self.reset()
        while not self.EOF:
            token = self._get_token()
            if token is not None:
                if token.check_token(_token_names.Ignored.names()):
                    if ignore:
                        continue
                yield token
