from ast import AST
from expression import Expression


class ExpressionsList(AST):
    def __init__(self):
        self.expressions: list(Expression)
