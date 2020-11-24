from __future__ import annotations

from .abstract_statement import AbstractStatement
from ..expressions.abstract_expression import AbstractExpression
from ..visitor import Visitor


class ReturnStatement(AbstractStatement):
    def __init__(self, expression: AbstractExpression):
        self.expression = expression

    def visit(self, visitor: Visitor, *args) -> object:
        return visitor.visit_return_statement(self, *args)
