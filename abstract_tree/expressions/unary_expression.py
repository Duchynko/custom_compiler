from __future__ import annotations

from .abstract_expression import AbstractExpression
from ..terminals.operator import Operator
from ..visitor import Visitor


class UnaryExpression(AbstractExpression):
    def __init__(self, operator: Operator, expression: AbstractExpression):
        self.operator = operator
        self.expression = expression

    def visit(self, visitor: Visitor) -> object:
        return visitor.visit_unary_expression(self)
