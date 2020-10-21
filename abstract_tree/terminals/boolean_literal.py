from .terminal import Terminal


class BooleanLiteral(Terminal):
    # self.values = ['true', 'false']

    def __init__(self, spelling: str):
        self.spelling = spelling
