from .abstract_expression import AbstractExpression
from ..terminals.operator import Operator
from ..visitor import Visitor


class BinaryExpression(AbstractExpression):
    def __init__(self, operator: Operator, expression1: AbstractExpression, expression2: AbstractExpression):
        self.operator = operator
        self.expression1 = expression1
        self.expression2 = expression2

    def visit(self, v: Visitor) -> object:
        return v.visit_binary_expression(self)
