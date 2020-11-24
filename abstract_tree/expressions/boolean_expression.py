from __future__ import annotations

from .abstract_expression import AbstractExpression
from ..terminals.boolean_literal import BooleanLiteral
from ..visitor import Visitor


class BooleanLiteralExpression(AbstractExpression):
    def __init__(self, literal: BooleanLiteral):
        self.literal = literal

    def visit(self, visitor: Visitor, *args) -> object:
        return visitor.visit_boolean_literal_expression(self, *args)
