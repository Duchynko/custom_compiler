from __future__ import annotations

from .abstract_statement import AbstractStatement
from ..expressions import AbstractExpression
from ..visitor import Visitor


class ExpressionStatement(AbstractStatement):
    def __init__(self, expressions: AbstractExpression):
        self.expressions = expressions

    def visit(self, visitor: Visitor) -> object:
        return visitor.visit_expression_statement(self)
