"""This is the module containing all codes needed for the lexer.

    This module would take the file and generate the tokens used by the parser.

    Example:
        >>> from lex import *
        >>> lexer = Lexer("./test/example.java") # Lexer takes the path to file
        >>> for token in lexer.tokens():
        >>>     print(token)
"""

from lex import token_names


class Symbol:
    def __init__(self, name, kind):
        super().__init__()
        self.name = name
        self.kind = kind

    __symbols = {}

    def toString(self):
        return self.name

    def getKind(self):
        return self.kind

    @staticmethod
    def symbol(newTokenStr, kind):
        s = Symbol.__symbols.get(newTokenStr)
        if s is None:
            if kind is None:
                return None
            s = Symbol(newTokenStr, kind)
            Symbol.__symbols[newTokenStr] = s
        return s

    @staticmethod
    def getSymbolsTable():
        return Symbol.__symbols

    def __str__(self):
        return f"{self.kind:20}\t {self.name}"

class Token(object):
    """ A simple Token structure.

        Contains the token position, name and value.

        Attributes:
            position (int): The start position of the token.
            token_name (str): The name of the token.
            value (str): The value of the token.
    """

    def __init__(self, leftPosition, rightPosition, symbol):
        self.leftPosition = leftPosition
        self.rightPosition = rightPosition
        self.symbol = symbol

    def __str__(self):
        return f"{self.leftPosition}\t {self.rightPosition}\t {self.symbol}"


class LexerError(Exception):
    """ Lexer error exception.

        Attributes:
            position (int): The start position of the error.
            message (str): The error message. Optional.
    """

    def __init__(self, position, message=None):
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

    def __init__(self, file):
        """
        Args:
            file: The path to the input file.
        """

        with open(file, 'r') as f:
            self.stream = f.read()
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
            if self._peek() == "*":  # Multiple-line comment
                while self.current_char != "*" or self._peek() != "/":
                    self._next_char()
                    if self.EOF:  # Check unclosed comment
                        raise LexerError(last_position, f"Unclosed comment at position {last_position}")
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

        # Checks single-quoted string.
        if self.current_char == "'":
            start_position = self.current_position
            while not (self.current_char != "\\" and self._peek() == "'"):
                self._next_char()
                if self.EOF:
                    raise LexerError(start_position, f"EOL while scanning string literal at position {start_position}")
            self._next_char()
            token = Token(start_position, self.current_position, Symbol.symbol(
                self.stream[start_position:self.current_position + 1], token_names.STRING))

        # Checks double-quoted string.
        elif self.current_char == '"':
            start_position = self.current_position
            while not (self.current_char != "\\" and self._peek() == '"'):
                self._next_char()
                if self.EOF:
                    raise LexerError(start_position, f"EOL while scanning string literal at position {start_position}")
            self._next_char()
            token = Token(start_position, self.current_position, Symbol.symbol(
                self.stream[start_position:self.current_position + 1], token_names.STRING))

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
            token = Token(start_position, self.current_position, Symbol.symbol(self.stream[start_position:self.current_position + 1], token_names.NUMBER))

        # Checks number begins with a dot.
        elif self.current_char == ".":
            if self._peek().isdigit():
                start_position = self.current_position
                while self._peek().isdigit():
                    self._next_char()
                if self._peek() in ["d", "D", "f", "F"]:
                    self._next_char()
                token = Token(start_position, self.current_position, Symbol.symbol(
                    self.stream[start_position:self.current_position + 1], token_names.NUMBER))
            else:
                token = Token(self.current_position, self.current_position, Symbol.symbol(
                    self.current_char, token_names.separators.get(self.current_char)))

        # Checks word begins with an alphabetic letter.
        elif self.current_char.isalpha():
            start_position = self.current_position
            while (self._peek() not in [" ", "\t", "\r", "\n", "\0"]
                    and self._peek() not in token_names.separators
                    and self._peek() not in token_names.operators):
                self._next_char()
            word = self.stream[start_position:self.current_position + 1]
            if word in token_names.keywords:    # Checks if word is a keyword.
                token = Token(start_position, self.current_position, Symbol.symbol(
                    word, token_names.keywords.get(word)))
            else:                               # Otherwise put it as identifier.
                token = Token(start_position, self.current_position,
                              Symbol.symbol(word, token_names.IDENTIFIER))

        # Checks if is a separator.
        elif self.current_char in token_names.separators:
            token = Token(self.current_position, self.current_position, Symbol.symbol(
                self.current_char, token_names.separators.get(self.current_char)))

        # Checks if is an operator.
        elif self.current_char in token_names.operators:
            last_position = self.current_position
            if self.current_char not in ["&", "|"] and self._peek() == "=":
                val = self.current_char + self._peek()
                self._next_char()
                token = Token(last_position, self.current_position, Symbol.symbol(
                    val, token_names.operators.get(val), ))
            elif self.current_char == "+" and self._peek() == "+":
                val = self.current_char + self._peek()
                self._next_char()
                token = Token(last_position, self.current_position,
                              Symbol.symbol(val, token_names.operators.get(val)))
            elif self.current_char == "-" and self._peek() == "-":
                val = self.current_char + self._peek()
                self._next_char()
                token = Token(last_position, self.current_position, Symbol.symbol(val, token_names.operators.get(val)))
            elif self.current_char == "&" and self._peek() == "&":
                val = self.current_char + self._peek()
                self._next_char()
                token = Token(last_position, self.current_position, Symbol.symbol(
                    val, token_names.operators.get(val)))
            elif self.current_char == "|" and self._peek() == "|":
                val = self.current_char + self._peek()
                self._next_char()
                token = Token(last_position, self.current_position, Symbol.symbol(
                    val, token_names.operators.get(val)))
            else:
                token = Token(self.current_position, self.current_position, Symbol.symbol(
                    self.current_char, token_names.operators.get(self.current_char)))

        # Checks if is EOF
        elif self.current_char == "\0":
            token = Token(self.current_position, self.current_position,
                          Symbol.symbol(self.current_char, token_names.EOF))

        # Raise error if is an unknown token.
        else:
            raise LexerError(self.current_position)

        self._next_char()
        return token

    # Generator function.
    def tokens(self):
        """ An generator to iterate over all of the tokens found in the character stream.

            Yields:
                Token: A token object.
            Raises:
                LexerError: An error occurred while getting tokens in the character stream.
        """

        while not self.EOF:
            token = self._get_token()
            yield token
