from .terminal import Terminal


class Identifier(Terminal):
    def __init__(self, spelling: str):
        self.spelling = spelling
