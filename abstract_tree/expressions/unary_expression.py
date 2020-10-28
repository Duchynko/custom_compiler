from abstract_tree.visitor import Visitor
from .abstract_expression import AbstractExpression
from ..terminals.operator import Operator


class UnaryExpression(AbstractExpression):
    def __init__(self, operator: Operator, expression: AbstractExpression):
        self.operator = operator
        self.expression = expression

    def visit(self, v: Visitor) -> object:
        return v.visit_unary_expression(self)
