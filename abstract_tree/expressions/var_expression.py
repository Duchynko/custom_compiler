from __future__ import annotations

from .abstract_expression import AbstractExpression
# from ..declarations import VarDeclaration
from ..terminals.identifier import Identifier
from ..visitor import Visitor


class VarExpression(AbstractExpression):
    def __init__(self, name: Identifier):
        self.name = name
        self.declaration = None

    def visit(self, visitor: Visitor, *args) -> object:
        return visitor.visit_var_expression(self, *args)
