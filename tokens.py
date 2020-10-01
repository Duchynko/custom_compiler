from enum import Enum, auto


class TokenType(Enum):
    INTEGER_LITERAL = auto()
    BOOLEAN_LITERAL = auto()
    OPERATOR = auto()
    FUNC = 'func'
    END = 'end'
    IF = 'if'
    THEN = 'then'
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
KEYWORDS: list(TokenType) = [
    TokenType.FUNC, TokenType.END,
    TokenType.IF, TokenType.THEN,
    TokenType.ELSE, TokenType.WHILE,
    TokenType.RETURN, TokenType.ECHO, TokenType.READ
]


class Token():
    def __init__(self, tokenType: TokenType, spelling: str):
        self.tokenType: TokenType = tokenType
        self.spelling: str = spelling

        # Check if and identifier is a keyword
        if self.tokenType == TokenType.IDENTIFIER:
            if self.spelling in [k.value for k in KEYWORDS]:
                self.tokenType = TokenType(self.spelling)

    def is_assign_operator(self):
        return self.is_type_of_operator(ASSIGNOPS)

    def is_mul_operator(self):
        return self.is_type_of_operator(MULOPS)

    def is_add_operator(self):
        return self.is_type_of_operator(ADDOPS)

    def is_type_of_operator(self, operators: list):
        if self.tokenType == TokenType.OPERATOR:
            return True if self.spelling in operators else False
        return False
