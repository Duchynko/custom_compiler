from .single_expression import SingleExpression
from ..terminals.operator import Operator


class BinaryExpression(SingleExpression):
    def __init__(self, operator: Operator, expression1: SingleExpression, expression2: SingleExpression):
        self.operator = operator
        self.expression1 = expression1
        self.expression2 = expression2
