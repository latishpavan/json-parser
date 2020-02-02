from enum import Enum, unique

class Symbols(Enum):
    CURLY_LBRACE = '{'
    CURLY_RBRACE = '}'
    SQUARE_LBRACE = '['
    SQUARE_RBRACE = ']'
    COLON = ':'
    COMMA = ','

class States(Enum):
    LVALUE = 'lvalue'
    RVALUE = 'rvalue'
