from __future__ import annotations

from .abstract_expression import AbstractExpression
from ..terminals.identifier import Identifier
from ..visitor import Visitor


class VarExpression(AbstractExpression):
    def __init__(self, name: Identifier):
        self.name = name

    def visit(self, visitor: Visitor) -> object:
        return visitor.visit_var_expression(self)
