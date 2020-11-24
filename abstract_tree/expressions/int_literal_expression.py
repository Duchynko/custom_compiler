from __future__ import annotations

from .abstract_expression import AbstractExpression
from ..terminals.integer_literal import IntegerLiteral
from ..visitor import Visitor


class IntLiteralExpression(AbstractExpression):
    def __init__(self, literal: IntegerLiteral):
        self.literal = literal

    def visit(self, visitor: Visitor, *args) -> object:
        return visitor.visit_int_literal_expression(self, *args)
