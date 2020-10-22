from enum import Enum, auto


class Kind(Enum):
    INTEGER_LITERAL = auto()
    OPERATOR = auto()
    STRING_TYPE = 'str'
    BOOLEAN_TYPE = 'bool'
    INTEGER_TYPE = 'int'
    TRUE = 'true'
    FALSE = 'false'
    FUNC = 'func'
    END = 'end'
    IF = 'if'
    ELSE = 'else'
    WHILE = 'while'
    RETURN = 'return'
    ECHO = 'echo'
    READ = 'read'
    LEFT_PAR = '('
    RIGHT_PAR = ')'
    SEMICOLON = ';'
    COLON = ':'
    QUOTE = '"'
    COMMA = ','
    IDENTIFIER = auto()
    EOT = ''
    ERROR = auto()


ASSIGNOPS: list = ['~']
ADDOPS: list = ['+', '-']
MULOPS: list = ['/', '*']
KEYWORDS: list(Kind) = [
    Kind.FUNC, Kind.END, Kind.ELSE,
    Kind.WHILE, Kind.IF, Kind.RETURN,
    Kind.ECHO, Kind.READ, Kind.TRUE,
    Kind.FALSE, Kind.STRING_TYPE,
    Kind.INTEGER_TYPE, Kind.BOOLEAN_TYPE
]
TYPE_DENOTERS: list(Kind) = [
    Kind.STRING_TYPE, Kind.INTEGER_TYPE,
    Kind.BOOLEAN_TYPE
]


class Token():
    def __init__(self, kind: Kind, spelling: str):
        self.kind: Kind = kind
        self.spelling: str = spelling

        # Check if and identifier is a keyword
        if self.kind == Kind.IDENTIFIER:
            if self.spelling in [k.value for k in KEYWORDS]:
                self.kind = Kind(self.spelling)

    def is_assign_operator(self):
        return self.is_type_of_operator(ASSIGNOPS)

    def is_mul_operator(self):
        return self.is_type_of_operator(MULOPS)

    def is_add_operator(self):
        return self.is_type_of_operator(ADDOPS)

    def is_type_of_operator(self, operators: list):
        if self.kind == Kind.OPERATOR:
            return True if self.spelling in operators else False
        return False
