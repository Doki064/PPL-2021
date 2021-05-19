"""Stores the names of all the token types."""

EOF = "EOF"
IDENTIFIER = "IDENTIFIER"
NUMBER = "LITERAL_NUMBER"
STRING = "LITERAL_STRING"

IGNORED = {
    "package": "KEYWORD_PACKAGE",
    "import": "KEYWORD_IMPORT",
}

KEYWORDS = {
    "this": "KEYWORD_THIS",
    "new": "KEYWORD_NEW",
    "return": "KEYWORD_RETURN",
    "if": "KEYWORD_IF",
    "else": "KEYWORD_ELSE",
    "switch": "KEYWORD_SWITCH",
    "case": "KEYWORD_CASE",
    "while": "KEYWORD_WHILE",
    "for": "KEYWORD_FOR",
    "break": "KEYWORD_BREAK",
    "continue": "KEYWORD_CONTINUE",
}

KEYWORDS_TYPE = {
    "class": "KEYWORD_CLASS",
    "var": "KEYWORD_VAR",
    "byte": "KEYWORD_BYTE",
    "short": "KEYWORD_SHORT",
    "int": "KEYWORD_INT",
    "long": "KEYWORD_LONG",
    "float": "KEYWORD_FLOAT",
    "double": "KEYWORD_DOUBLE",
    "char": "KEYWORD_CHAR",
    "String": "KEYWORD_STRING",
    "boolean": "KEYWORD_BOOLEAN",
    "void": "KEYWORD_VOID",
}

KEYWORDS_ATTRIBUTE = {
    "public": "KEYWORD_PUBLIC",
    "private": "KEYWORD_PRIVATE",
    "protected": "KEYWORD_PROTECTED",
    "static": "KEYWORD_STATIC",
    "final": "KEYWORD_FINAL",
}

OPERATORS = {
    "+": "OP_ADD",
    "-": "OP_SUB",
    "*": "OP_MUL",
    "/": "OP_DIV",
    "%": "OP_MOD",
    "++": "OP_INCREMENT",
    "--": "OP_DECREMENT",
    "&": "OP_BIT_AND",
    "|": "OP_BIT_OR",
    "^": "OP_BIT_XOR",
    "<": "OP_LT",
    "<=": "OP_LTE",
    ">": "OP_GT",
    ">=": "OP_GTE",
    "==": "OP_EQ",
    "!=": "OP_NEQ",
    "!": "OP_NOT",
    "=": "OP_ASSIGN",
    "+=": "OP_ADD_ASSIGN",
    "-=": "OP_SUB_ASSIGN",
    "*=": "OP_MUL_ASSIGN",
    "/=": "OP_DIV_ASSIGN",
    "%=": "OP_MOD_ASSIGN",
    "&&": "OP_LOGIC_AND",
    "||": "OP_LOGIC_OR",
}

SEPARATORS = {
    "(": "SEP_PAREN_LEFT",
    ")": "SEP_PAREN_RIGHT",
    "[": "SEP_BRACKET_LEFT",
    "]": "SEP_BRACKET_RIGHT",
    "{": "SEP_BRACE_LEFT",
    "}": "SEP_BRACE_RIGHT",
    ":": "SEP_COLON",
    ";": "SEP_SEMICOLON",
    ",": "SEP_COMMA",
    ".": "SEP_DOT",
}
