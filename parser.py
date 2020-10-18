from scanner import Scanner
from tokens import Kind as K
from exceptions import (UnexpectedTokenException,
                        UnsupportedExpressionTokenException,
                        UnsupportedCommandTokenException,
                        UnsupportedDeclarationTokenException,
                        UnexpectedEndOfProgramException)


class Parser():
    def __init__(self, scanner: Scanner):
        self.scanner = scanner
        self.current_terminal = scanner.scan()

    def parse_program(self):
        self.parse_command()

        if self.current_terminal.kind is not K.EOT:
            raise UnexpectedEndOfProgramException(self.current_terminal)
        print(f"Successfully parsed the program.")

    def parse_command(self):
        while self.current_terminal.kind in [K.IDENTIFIER, K.FUNC,
                                             K.IF, K.WHILE, K.RETURN]:
            self.parse_single_command()

    def parse_single_command(self):
        if self.current_terminal.kind is K.FUNC:
            self.parse_declaration()
        elif self.current_terminal.kind is K.RETURN:
            self.accept(K.RETURN)
            self.parse_expression()
        elif self.current_terminal.kind is K.IF:
            self.accept(K.IF)
            self.accept(K.LEFT_PAR)
            self.parse_expression()
            self.accept(K.RIGHT_PAR)
            self.accept(K.COLON)
            self.parse_command()
            if self.current_terminal.kind is K.ELSE:
                self.accept(K.ELSE)
                self.accept(K.COLON)
                self.parse_command()
            self.accept(K.END)
        elif self.current_terminal.kind is K.WHILE:
            self.accept(K.WHILE)
            self.accept(K.LEFT_PAR)
            self.parse_expression()
            self.accept(K.RIGHT_PAR)
            self.accept(K.COLON)
            self.parse_command()
            self.accept(K.END)
        elif self.current_terminal.kind is K.IDENTIFIER:
            if self.current_terminal.spelling in ['int', 'str', 'bool']:
                self.parse_declaration()
                self.accept(K.SEMICOLON)
            else:
                self.parse_expression()
                self.accept(K.SEMICOLON)
        else:
            raise UnsupportedCommandTokenException(
                current_token=self.current_terminal,
                current_line=self.scanner.current_line,
                current_column=self.scanner.current_column
            )

    def parse_declaration(self):
        while (self.current_terminal.kind is K.FUNC
                or self.current_terminal.spelling in ['int', 'str', 'bool']):
            self.parse_single_declaration()

    def parse_single_declaration(self):
        if self.current_terminal.kind is K.FUNC:
            self.accept(K.FUNC)
            self.accept(K.IDENTIFIER)
            self.accept(K.LEFT_PAR)
            if self.current_terminal.kind in [K.IDENTIFIER, K.INTEGER_LITERAL, K.BOOLEAN_LITERAL]:
                self.parse_single_expression()
                while self.current_terminal.kind is K.COMMA:
                    self.accept(K.COMMA)
                    self.parse_single_expression()
            self.accept(K.RIGHT_PAR)
            self.accept(K.COLON)
            self.parse_command()
            self.accept(K.END)
        elif self.current_terminal.kind is K.IDENTIFIER:
            self.parse_type_denoter()
            self.accept(K.IDENTIFIER)
            if self.current_terminal.kind is K.OPERATOR:
                self.accept(K.OPERATOR)
                self.parse_expression()
        else:
            raise UnsupportedDeclarationTokenException(
                current_token=self.current_terminal,
                current_line=self.scanner.current_line,
                current_column=self.scanner.current_column
            )

    def parse_expression(self):
        self.parse_single_expression()
        while self.current_terminal.kind is K.OPERATOR:
            self.parse_single_expression()

    def parse_single_expression(self):
        if self.current_terminal.kind is K.INTEGER_LITERAL:
            self.accept(K.INTEGER_LITERAL)
        elif self.current_terminal.kind is K.RETURN:
            self.accept(K.RETURN)
            # TODO: Add return Expression
            self.accept(K.IDENTIFIER)
        elif self.current_terminal.kind is K.BOOLEAN_LITERAL:
            self.accept(K.BOOLEAN_LITERAL)
        elif self.current_terminal.kind is K.OPERATOR:
            self.accept(K.OPERATOR)
            self.parse_single_expression()
        elif self.current_terminal.kind is K.IDENTIFIER:
            self.accept(K.IDENTIFIER)
            # identifier()
            if self.current_terminal.kind is K.LEFT_PAR:
                self.accept(K.LEFT_PAR)
                if self.current_terminal.kind in [K.IDENTIFIER, K.INTEGER_LITERAL, K.OPERATOR, K.BOOLEAN_LITERAL]:
                    self.parse_single_expression()
                    while self.current_terminal.kind is K.COMMA:
                        self.accept(K.COMMA)
                        self.parse_single_expression()
                self.accept(K.RIGHT_PAR)
            # identifier ~ expression
            elif self.current_terminal.kind is K.OPERATOR:
                self.parse_expression()
        else:
            raise UnsupportedExpressionTokenException(
                current_token=self.current_terminal,
                current_line=self.scanner.current_line,
                current_column=self.scanner.current_column
            )

    def parse_type_denoter(self):
        self.accept(K.IDENTIFIER)

    def accept(self, token: K):
        if self.current_terminal.kind is token:
            self.current_terminal = self.scanner.scan()
            return True
        else:
            # return False
            raise UnexpectedTokenException(
                expected_kind=token,
                current_token=self.current_terminal,
                current_line=self.scanner.current_line,
                current_column=self.scanner.current_column
            )
