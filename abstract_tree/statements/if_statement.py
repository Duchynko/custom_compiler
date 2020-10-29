from __future__ import annotations

from .abstract_statement import AbstractStatement
from ..commands import CommandList
from ..expressions import AbstractExpression
from ..visitor import Visitor


class IfStatement(AbstractStatement):
    def __init__(self, expr: AbstractExpression, if_com: CommandList, else_com: CommandList):
        self.expr = expr
        self.if_com = if_com
        self.else_com = else_com

    def visit(self, visitor: Visitor) -> object:
        return visitor.visit_if_statement(self)
