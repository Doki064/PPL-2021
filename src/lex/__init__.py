"""This is the module containing all codes needed for the lexer.

    This module would take the character stream and generate a collection of tokens.

    Example:
        >>> from lex import Lexer
        >>> with open(path_to_file, "r") as f:
        >>>     character_stream = f.read()
        >>> lexer = Lexer(character_stream)
        >>> for token in lexer.tokens():
        >>>     print(token)
"""

from typing import Iterator

try:
    from lex import _token_names
except Exception:
    from src.lex import _token_names

token_names = _token_names


class Token:
    # """ A simple Token structure.

    #     Contains the token position, name and value.
    # """

    def __init__(self, start_position, end_position, token_name, value):
        """Token constructor.

            Args:
                start_position (int): The start position of the token.
                end_position (int): The end position of the token.
                token_name (str): The name of the token.
                value (str): The value of the token.
        """

        self.position = self.start_position = start_position
        self.end_position = end_position
        self.token_name = token_name
        self.value = value

    def __str__(self):
        return f"{self.start_position}\t {self.end_position}\t {self.token_name}\t {self.value}"

    def __hash__(self):
        return hash((self.position, self.token_name, self.value))

    def __eq__(self, other):
        if isinstance(other, Token):
            return self.position == other.position and self.token_name == other.token_name and self.value == other.value
        return NotImplemented


class LexerError(Exception):
    """ Lexer exception."""

    def __init__(self, position, message=None):
        """LexerError constructor.

            Args:
                position (int): The start position of the error.
                message (str): The error message. Optional.
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
            while (self._peek() not in [" ", "\t", "\r", "\n", "\0"]
                   and self._peek() not in _token_names.SEPARATORS
                   and self._peek() not in _token_names.OPERATORS):
                self._next_char()
            word = self.stream[start_position:self.current_position + 1]
            # Checks if word is ignored.
            if word in _token_names.Ignored.Keywords.values():
                while self.current_char != ";":
                    self._next_char()
            elif word in _token_names.Ignored.KeywordsAttribute.values():
                self._next_char()
            # Checks if word is a keyword.
            elif word in _token_names.Keywords.values():
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

    # Generator function.
    def tokens(self) -> Iterator[Token]:
        """ An generator to iterate over all of the tokens found in the character stream.

            Yields:
                Token: A token object.
            Raises:
                LexerError: An error occurred while getting tokens in the character stream.
        """

        while not self.EOF:
            token = self._get_token()
            if token is not None:
                yield token
