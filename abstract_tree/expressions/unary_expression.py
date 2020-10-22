from .single_expression import SingleExpression
from ..terminals.operator import Operator


class UnaryExpression(SingleExpression):
    def __init__(self, operator: Operator, expression: SingleExpression):
        self.operator = operator
        self.expression = expression
