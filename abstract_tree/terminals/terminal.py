from ..ast import AST


class Terminal(AST):
    def __init__(self):
        self.spelling: str
