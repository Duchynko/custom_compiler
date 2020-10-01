from scanner import Scanner
from tokens import TokenType as T


class Parser():
    def __init__(self, scanner: Scanner):
        self.scanner = scanner
        self.current_terminal = scanner.scan()

    def parse_program(self):
        self.parse_command()

        if self.current_terminal.tokenType is not T.EOT:
            print(f"Couldn't parse the program. A token found after end of program")

    def parse_command(self):
        while self.current_terminal.tokenType in [T.IDENTIFIER, T.FUNC,
                                                  T.IF, T.WHILE, T.RETURN]:
            self.parse_single_command()

    def parse_single_command(self):
        if self.current_terminal.tokenType is T.FUNC:
            self.parse_declaration()
        elif self.current_terminal.tokenType is T.RETURN:
            self.accept(T.RETURN)
            self.parse_expression()
        elif self.current_terminal.tokenType is T.IF:
            self.accept(T.IF)
            self.accept(T.LEFT_PAR)
            self.parse_expression()
            self.accept(T.RIGHT_PAR)
            self.accept(T.COLON)
            self.parse_command()
            self.accept(T.SEMICOLON)
            if self.current_terminal.tokenType is T.ELSE:
                self.accept(T.ELSE)
                self.accept(T.COLON)
                self.parse_command()
                self.accept(T.SEMICOLON)
            self.accept(T.END)
        elif self.current_terminal.tokenType is T.WHILE:
            self.accept(T.WHILE)
            self.accept(T.LEFT_PAR)
            self.parse_expression()
            self.accept(T.RIGHT_PAR)
            self.parse_command()
            self.accept(T.SEMICOLON)
            self.accept(T.END)
        elif self.current_terminal.tokenType is T.IDENTIFIER:
            if self.current_terminal.spelling in ['int', 'str', 'bool']:
                self.parse_declaration()
            else:
                self.accept(T.IDENTIFIER)
                # function call
                if self.current_terminal.tokenType is T.LEFT_PAR:
                    self.accept(T.LEFT_PAR)
                    if self.current_terminal.tokenType in [T.IDENTIFIER, T.INTEGER_LITERAL, T.OPERATOR, T.BOOLEAN_LITERAL]:
                        self.parse_single_expression()
                        while self.current_terminal.tokenType is T.COMMA:
                            self.accept(T.COMMA)
                            self.parse_single_expression()
                    self.accept(T.RIGHT_PAR)
        else:
            raise Exception(
                f"Unexpected token {self.current_terminal.spelling}")

    def parse_declaration(self):
        while self.current_terminal.tokenType in [T.IDENTIFIER, T.FUNC]:
            self.parse_single_declaration()

    def parse_single_declaration(self):
        if self.current_terminal.tokenType is T.IDENTIFIER:
            self.accept(T.IDENTIFIER)  # type-denoter
            self.accept(T.IDENTIFIER)
            if self.current_terminal.tokenType is T.OPERATOR:
                self.accept(T.OPERATOR)
                self.parse_expression()
            self.accept(T.SEMICOLON)
        elif self.current_terminal.tokenType is T.FUNC:
            self.accept(T.FUNC)
            self.accept(T.IDENTIFIER)
            self.accept(T.LEFT_PAR)
            self.parse_expression()
            self.accept(T.RIGHT_PAR)
            self.accept(T.COLON)
            self.parse_command()
            self.accept(T.END)

    def parse_expression(self):
        self.parse_single_expression()
        while self.current_terminal.tokenType is T.OPERATOR:
            self.parse_single_expression()

    def parse_single_expression(self):
        if self.current_terminal.tokenType is T.INTEGER_LITERAL:
            self.accept(T.INTEGER_LITERAL)
        elif self.current_terminal.tokenType is T.RETURN:
            self.accept(T.RETURN)
            self.accept(T.IDENTIFIER)
        elif self.current_terminal.tokenType is T.BOOLEAN_LITERAL:
            self.accept(T.BOOLEAN_LITERAL)
        elif self.current_terminal.tokenType is T.OPERATOR:
            self.accept(T.OPERATOR)
            self.parse_single_expression()
        elif self.current_terminal.tokenType is T.IDENTIFIER:
            self.accept(T.IDENTIFIER)
        else:
            raise Exception(
                f"Unexpected expression token {self.current_terminal.spelling}")

    def parse_type_denoter(self):
        self.accept(T.IDENTIFIER)

    def accept(self, token: T):
        if self.current_terminal.tokenType is token:
            self.current_terminal = self.scanner.scan()
            return True
        else:
            print(
                f"Expected token {token}, got {self.current_terminal.spelling} ({self.current_terminal.tokenType})")
            return False
