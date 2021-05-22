"""Stores the names of all the token types."""

__all__ = [
    "EOF",
    "IDENTIFIER",
    "NUMBER",
    "STRING",
    "Ignored",
    "Keywords",
    "KeywordsType",
    "KeywordsAttribute",
    "Operators",
    "Separators",
    "names",
    "values",
    "to_dict",
    "items",
    "get_value_by_name",
    "code_mapper",
]

from enum import Enum as _Enum

try:
    from mapper import code_mapper
except ImportError:
    from src.mapper import code_mapper

# Must keep!
EOF = "EOF"
IDENTIFIER = "IDENTIFIER"
NUMBER = "LITERAL_NUMBER"
STRING = "LITERAL_STRING"


def names():
    return (
            Keywords.names() +
            KeywordsType.names() +
            KeywordsAttribute.names() +
            Operators.names() +
            Separators.names()
    )


def values():
    return (
            Keywords.values() +
            KeywordsType.values() +
            KeywordsAttribute.values() +
            Operators.values() +
            Separators.values()
    )


def to_dict():
    return {
        **Keywords.to_dict(),
        **KeywordsType.to_dict(),
        **KeywordsAttribute.to_dict(),
        **Operators.to_dict(),
        **Separators.to_dict(),
    }


def items():
    return to_dict().items()


def get_value_by_name(name):
    try:
        return to_dict()[name]
    except KeyError:
        return None


class _BaseEnum(_Enum):
    @classmethod
    def names(cls):
        return [member.name for member in cls]

    @classmethod
    def values(cls):
        return [member.value for member in cls]

    @classmethod
    def to_dict(cls):
        return dict((member.name, member.value) for member in cls)

    @classmethod
    def items(cls):
        return cls.to_dict().items()


class Ignored(_BaseEnum):
    # Keywords
    KEYWORD_PACKAGE = "package"
    KEYWORD_IMPORT = "import"
    KEYWORD_NEW = "new"

    # Attributes
    KEYWORD_PUBLIC = "public"
    KEYWORD_PRIVATE = "private"
    KEYWORD_PROTECTED = "protected"
    KEYWORD_ABSTRACT = "abstract"
    KEYWORD_STATIC = "static"


class Keywords(_BaseEnum):
    KEYWORD_PACKAGE = "package"
    KEYWORD_IMPORT = "import"
    KEYWORD_NEW = "new"
    KEYWORD_THIS = "this"
    KEYWORD_RETURN = "return"
    KEYWORD_TRY = "try"
    KEYWORD_CATCH = "catch"
    KEYWORD_FINALLY = "finally"
    KEYWORD_IF = "if"
    KEYWORD_ELSE = "else"
    KEYWORD_SWITCH = "switch"
    KEYWORD_CASE = "case"
    KEYWORD_DEFAULT = "default"
    KEYWORD_WHILE = "while"
    KEYWORD_FOR = "for"
    KEYWORD_BREAK = "break"
    KEYWORD_CONTINUE = "continue"


class KeywordsType(_BaseEnum):
    KEYWORD_CLASS = "class"
    KEYWORD_VAR = "var"
    KEYWORD_BYTE = "byte"
    KEYWORD_SHORT = "short"
    KEYWORD_INT = "int"
    KEYWORD_LONG = "long"
    KEYWORD_FLOAT = "float"
    KEYWORD_DOUBLE = "double"
    KEYWORD_CHAR = "char"
    KEYWORD_STRING = "String"
    KEYWORD_BOOLEAN = "boolean"
    KEYWORD_VOID = "void"


class KeywordsAttribute(_BaseEnum):
    KEYWORD_FINAL = "final"
    KEYWORD_PUBLIC = "public"
    KEYWORD_PRIVATE = "private"
    KEYWORD_PROTECTED = "protected"
    KEYWORD_ABSTRACT = "abstract"
    KEYWORD_STATIC = "static"


class Operators(_BaseEnum):
    OP_ADD = "+"
    OP_SUB = "-"
    OP_MUL = "*"
    OP_DIV = "/"
    OP_MOD = "%"
    OP_INCREMENT = "++"
    OP_DECREMENT = "--"
    OP_BIT_AND = "&"
    OP_BIT_OR = "|"
    OP_BIT_XOR = "^"
    OP_LT = "<"
    OP_LTE = "<="
    OP_GT = ">"
    OP_GTE = ">="
    OP_EQ = "=="
    OP_NEQ = "!="
    OP_NOT = "!"
    OP_ASSIGN = "="
    OP_ADD_ASSIGN = "+="
    OP_SUB_ASSIGN = "-="
    OP_MUL_ASSIGN = "*="
    OP_DIV_ASSIGN = "/="
    OP_MOD_ASSIGN = "%="
    OP_LOGIC_AND = "&&"
    OP_LOGIC_OR = "||"


class Separators(_BaseEnum):
    SEP_PAREN_LEFT = "("
    SEP_PAREN_RIGHT = ")"
    SEP_BRACKET_LEFT = "["
    SEP_BRACKET_RIGHT = "]"
    SEP_BRACE_LEFT = "{"
    SEP_BRACE_RIGHT = "}"
    SEP_COLON = ":"
    SEP_SEMICOLON = ";"
    SEP_COMMA = ","
