from __future__ import annotations

from .abstract_syntax_tree import AbstractSyntaxTree
from .commands import CommandList
from .visitor import Visitor


class Program(AbstractSyntaxTree):
    def __init__(self, command_list: CommandList):
        self.command_list = command_list

    def visit(self, visitor: Visitor, *args):
        return visitor.visit_program(self, args)
