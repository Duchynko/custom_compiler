from tokens import Kind, Token


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
        self.current_char = self.source.get_next_char()
        self.current_line = 1
        self.current_column = 0

    def __count_position(self) -> None:
        if self.current_char == '\n':
            self.current_line = self.current_line + 1
            self.current_column = 0
        else:
            self.current_column = self.current_column + 1

    def scan(self) -> Token:
        """
        Scans through characters, finds the next token and returns it as a Token object.
        """
        while self.current_char in ['#', '\n', '\t', '\r', ' ']:
            self.discard_separator()

        self.current_spelling.clear()
        kind: Kind = self.scan_token()

        return Token(kind, "".join(self.current_spelling))

    def scan_token(self) -> Kind:
        """
        Scans through the current character(s) and returns it's kind
        """
        if self.current_char.isalpha():
            self.take_it()
            while self.current_char.isalpha() or self.current_char.isdigit():
                self.take_it()
            return Kind.IDENTIFIER

        elif self.current_char.isdigit():
            self.take_it()
            while self.current_char.isdigit():
                self.take_it()
            return Kind.INTEGER_LITERAL

        elif self.current_char == SourceFile.EOT:
            return Kind.EOT

        elif self.current_char == '=':
            self.take_it()
            if self.current_char == '=':
                self.take_it()
                return Kind.OPERATOR
            else:
                return Kind.ERROR

        else:
            char = self.current_char
            self.take_it()
            return {
                '~': Kind.OPERATOR,
                '+': Kind.OPERATOR,
                '-': Kind.OPERATOR,
                '/': Kind.OPERATOR,
                '*': Kind.OPERATOR,
                ';': Kind.SEMICOLON,
                '(': Kind.LEFT_PAR,
                ')': Kind.RIGHT_PAR,
                '"': Kind.QUOTE,
                ':': Kind.COLON,
                ',': Kind.COMMA
            }.get(char, Kind.ERROR)

    def discard_separator(self):
        """
        Discards the current character and moves the pointer to the next one, or if the
        curret character is a comment symbol (#), moves the pointer to the next line.
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
        self.__count_position()
