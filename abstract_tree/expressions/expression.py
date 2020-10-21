from ..ast import AST
from .single_expression import SingleExpression


class Expression(AST):
    def __init__(self):
        self.expressions: list(SingleExpression)
