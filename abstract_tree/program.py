from __future__ import annotations

from .abstract_syntax_tree import AbstractSyntaxTree
from .commands import CommandList
from .visitor import Visitor


class Program(AbstractSyntaxTree):
    def __init__(self, command: CommandList):
        self.command = command

    def visit(self, visitor: Visitor):
        return visitor.visit_program(self)
