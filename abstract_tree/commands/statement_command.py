from __future__ import annotations

from .abstract_command import AbstractCommand
from ..statements.abstract_statement import AbstractStatement
from ..visitor import Visitor


class StatementCommand(AbstractCommand):
    def __init__(self, statement: AbstractStatement):
        self.statement = statement

    def visit(self, visitor: Visitor) -> object:
        return visitor.visit_statement_command(self)
