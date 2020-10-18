from tokens import Token
from abc import ABC


class UnexpectedEndOfProgramException(Exception):
    """
    An exception thrown when a program wasn't parsed successfully. This
    happens if a parser won't find an EOT token at the end of a program.

    Args:
        current_token: current token parsed by a parser
    """

    def __init__(self, current_token: Token):
        self.message = (f"Couldn't parse the program. A token {current_token.kind.name} "
                        f"({current_token.spelling}) found after the end of the program")
        super.__init__()


class UnexpectedTokenException(Exception):
    """
    An exception thrown when a parser expects a different token kind 
    than the current terminal is.

    Args:
        expected: token expected by parser
        actual: actual supplied token
        current_line: line on which parser found an unexpected token
        current_column: column on which parser found an unexpected token
    """

    def __init__(self, expected: Token, actual: Token, current_line: int, current_column: int):
        self.line = current_line
        self.column = current_column
        self.message = (
            f"Error on line {current_line}, column {current_column}.\n"
            f"Expected token {expected.kind.name}, got {actual.kind.name} ({actual.spelling})"
        )

        super().__init__(self.message)


class UnsupportedTokenException(ABC, Exception):
    def __init__(self, symbol_type: str, current_token: Token, current_line: int, current_column: int):
        self.line = current_line
        self.column = current_column
        self.symbol_type = symbol_type.lower()
        self.message = (
            f"Error on line {current_line}, column {current_column}.\n"
            f"Unexpected {self.symbol_type} token {current_token.kind.name} ({current_token.spelling})"
        )

        super().__init__(self.message)


class UnsupportedExpressionTokenException(UnsupportedTokenException):
    """
    An exception thrown when a parser receives an unexpected token inside of
    the parse_single_expression() method.

    Args:
        current_token: current token parsed by a parser
        current_line: line on which parser found an unexpected token
        current_column: column on which parser found an unexpected token
    """

    def __init__(self, current_token: Token, current_line: int, current_column: int):
        super().__init__(symbol_type='expression')


class UnsupportedCommandTokenException(UnsupportedTokenException):
    """
    An exception thrown when a parser receives an unexpected token inside of
    the parse_single_command() method.

    Args:
        current_token: current token parsed by a parser
        current_line: line on which parser found an unexpected token
        current_column: column on which parser found an unexpected token
    """

    def __init__(self, current_token: Token, current_line: int, current_column: int):
        super().__init__(symbol_type='command')


class UnsupportedDeclarationTokenException(UnsupportedTokenException):
    """
    An exception thrown when a parser receives an unexpected token inside of
    the parse_single_declaration() method.

    Args:
        current_token: current token parsed by a parser
        current_line: line on which parser found an unexpected token
        current_column: column on which parser found an unexpected token
    """

    def __init__(self, current_token: Token, current_line: int, current_column: int):
        super().__init__(symbol_type='declaration')
