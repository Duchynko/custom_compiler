from .terminal import Terminal


class IntegerLiteral(Terminal):
    def __init__(self, spelling: str):
        self.spelling = spelling
