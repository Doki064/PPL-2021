""""""
from lex import token_names


class Token(object):
    """ A simple Token structure.

        Contains the token position, name and value.

        Attributes:
            position: the start position of the token.
            token_name: the name of the token.
            value: the value of the token.
    """

    def __init__(self, position, token_name, value):
        self.position = position
        self.token_name = token_name
        self.value = value

    def __str__(self):
        return f"{self.position}\t {self.token_name}\t {self.value}"


class LexerError(Exception):
    """ Lexer error exception.

        Attributes:
            position: the start position of the error.
            message: the error message. Default is None.
    """

    def __init__(self, position, message=None):
        self.position = position
        self.message = f"Unknown token at position {self.position}" if message is None else message
        super().__init__(self.message)


class Lexer:
    """The lexer.

        Scans the file as stream and tokenize it.

        Attributes:
            stream: the data to work on.
            EOF: the flag to indicate end of file.
            symbol_table: stores the identifiers and their types.
            current_position: the position in the stream currently.
            current_char: the current character.
    """

    def __init__(self, file=None):
        """
        Args:
            file: the input file.
        """

        with open(file, 'r') as f:
            self.stream = f.read()
        self.EOF = False
        self.current_position = -1
        self.current_char = ""
        self._next_char()

    # Moves to the next character.
    def _next_char(self):
        self.current_position += 1
        if self.current_position >= len(self.stream):
            self.current_char = ""
            self.EOF = True
        else:
            self.current_char = self.stream[self.current_position]

    # Returns the lookahead character.
    def _peek(self):
        if self.current_position + 1 >= len(self.stream):
            return ""
        return self.stream[self.current_position + 1]

    # Skips whitespaces, newlines and comments.
    def _skip(self):
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

    # Returns the next token.
    def _get_token(self):
        self._skip()

        token = None

        # Checks single-quoted string.
        if self.current_char == "'":
            start_position = self.current_position
            while not (self.current_char != "\\" and self._peek() == "'"):
                self._next_char()
                if self.EOF:
                    raise LexerError(start_position, f"EOL while scanning string literal at position {start_position}")
            self._next_char()
            token = Token(start_position, token_names.STRING, self.stream[start_position:self.current_position + 1])

        # Checks double-quoted string.
        elif self.current_char == '"':
            start_position = self.current_position
            while not (self.current_char != "\\" and self._peek() == '"'):
                self._next_char()
                if self.EOF:
                    raise LexerError(start_position, f"EOL while scanning string literal at position {start_position}")
            self._next_char()
            token = Token(start_position, token_names.STRING, self.stream[start_position:self.current_position + 1])

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
            token = Token(start_position, token_names.NUMBER, self.stream[start_position:self.current_position + 1])

        # Checks number begins with a dot.
        elif self.current_char == ".":
            if self._peek().isdigit():
                start_position = self.current_position
                while self._peek().isdigit():
                    self._next_char()
                if self._peek() in ["d", "D", "f", "F"]:
                    self._next_char()
                token = Token(start_position, token_names.NUMBER, self.stream[start_position:self.current_position + 1])
            else:
                token = Token(self.current_position, token_names.separators.get(self.current_char), self.current_char)

        # Checks word begins with an alphabetic letter.
        elif self.current_char.isalpha():
            start_position = self.current_position
            while self._peek() not in ["", " ", "\t", "\r", "\n"] \
                    and self._peek() not in token_names.separators \
                    and self._peek() not in token_names.operators:
                self._next_char()
            word = self.stream[start_position:self.current_position + 1]
            if word in token_names.keywords:    # Checks if word is a keyword.
                token = Token(start_position, token_names.keywords.get(word), word)
            else:                               # Otherwise put it as identifier.
                token = Token(start_position, token_names.IDENTIFIER, word)

        # Checks if is a separator.
        elif self.current_char in token_names.separators:
            token = Token(self.current_position, token_names.separators.get(self.current_char), self.current_char)

        # Checks if is an operator.
        elif self.current_char in token_names.operators:
            last_position = self.current_position
            if self.current_char not in ["&", "|"] and self._peek() == "=":
                val = self.current_char + self._peek()
                self._next_char()
                token = Token(last_position, token_names.operators.get(val), val)
            elif self.current_char == "+" and self._peek() == "+":
                val = self.current_char + self._peek()
                self._next_char()
                token = Token(last_position, token_names.operators.get(val), val)
            elif self.current_char == "-" and self._peek() == "-":
                val = self.current_char + self._peek()
                self._next_char()
                token = Token(last_position, token_names.operators.get(val), val)
            elif self.current_char == "&" and self._peek() == "&":
                val = self.current_char + self._peek()
                self._next_char()
                token = Token(last_position, token_names.operators.get(val), val)
            elif self.current_char == "|" and self._peek() == "|":
                val = self.current_char + self._peek()
                self._next_char()
                token = Token(last_position, token_names.operators.get(val), val)
            else:
                token = Token(self.current_position, token_names.operators.get(self.current_char), self.current_char)

        # Checks if is EOF
        elif self.current_char == "":
            token = Token(self.current_position, token_names.EOF, self.current_char)

        # Raise error if is an unknown token.
        else:
            raise LexerError(self.current_position)

        self._next_char()
        return token

    # Iterator function.
    def tokens(self):
        """Returns an iterator to the tokens found in the file."""
        while not self.EOF:
            token = self._get_token()
            yield token
