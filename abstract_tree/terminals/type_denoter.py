from .terminal import Terminal


class TypeDenoter(Terminal):
    def __init__(self, spelling: str):
        self.spelling = spelling
