from enum import Enum, auto


class TokenType(Enum):
    IDENTIFIER = auto()
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
    RIGHT_PAR = '('
    SEMICOLON = ';'
    QUOTE = '"'
    EOT = auto()
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
    def __init__(self, tokenType, spelling):
        self.tokenType: TokenType = tokenType
        self.spelling: str = spelling

        # Check if and identifier is a keyword
        if self.tokenType == TokenType.IDENTIFIER:
            if self.spelling in [k.value for k in KEYWORDS]:
                self.tokenType = TokenType(self.spelling)

    def is_assign_operator(self):
        return True
