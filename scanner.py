from tokens import TokenType, Token


class SourceFile:
    EOL = '\n'
    EOT = ''

    def __init__(self, filename):
        try:
            self.source = open(filename, 'r')
        except OSError as oserr:
            print(oserr)
            exit(1)

    def get_next_char(self):
        char = self.source.read(1)
        if not char:
            return self.EOT
        return char


class Scanner:
    def __init__(self, source):
        self.source = SourceFile(source)
        self.current_spelling: list(str) = []
        self.current_char: str = self.source.get_next_char()

    def scan(self) -> Token:
        """
        Scans through characters, finds the next token and returns it as a Token object.
        """
        while self.current_char in ['#', '\n', '\t', '\r', ' ']:
            self.discard_separator()

        self.current_spelling.clear()
        tokenType: TokenType = self.scan_token()

        return Token(tokenType, self.current_spelling)

    def scan_token(self):
        if self.current_char.isalpha():
            self.take_it()
            while self.current_char.isalpha() or self.current_char.isdigit():
                self.take_it()
            return TokenType.IDENTIFIER

        elif self.current_char.isdigit():
            self.take_it()
            while self.current_char.isdigit():
                self.take_it()
            return TokenType.INTEGER_LITERAL

        elif self.current_char == SourceFile.EOT:
            return TokenType.EOT

        elif self.current_char == '=':
            self.take_it()
            if self.current_char == '=':
                self.take_it()
                return TokenType.OPERATOR
            else:
                return TokenType.ERROR

        else:
            char = self.current_char
            self.take_it()
            return {
                '~': TokenType.OPERATOR,
                '+': TokenType.OPERATOR,
                '-': TokenType.OPERATOR,
                '/': TokenType.OPERATOR,
                '*': TokenType.OPERATOR,
                ';': TokenType.SEMICOLON,
                '(': TokenType.LEFT_PAR,
                ')': TokenType.RIGHT_PAR,
                '"': TokenType.QUOTE
            }.get(char, TokenType.ERROR)

    def discard_separator(self):
        """
        Checks the current character and moves the pointer to the next one, or
        if the curret character is a comment symbol (#), moves the pointer to a new line.
        """
        if self.current_char == '#':
            self.take_it()
            while self.current_char not in [SourceFile.EOL, SourceFile.EOT]:
                self.take_it()

            if self.current_char == SourceFile.EOL:
                self.take_it()
        else:
            self.take_it()

    def take_it(self):
        self.current_spelling.append(self.current_char)
        self.current_char = str(self.source.get_next_char())
