from __future__ import annotations

from .abstract_statement import AbstractStatement
from ..commands import CommandList
from ..expressions import AbstractExpression
from ..visitor import Visitor


class WhileStatement(AbstractStatement):
    def __init__(self, expr: AbstractExpression, command: CommandList):
        self.command = command
        self.expr = expr

    def visit(self, visitor: Visitor) -> object:
        return visitor.visit_while_statement(self)
