from ..ast import AST
from .single_statement import SingleStatement


class Statement(AST):
    def __init__(self):
        self.statements: list(SingleStatement)
