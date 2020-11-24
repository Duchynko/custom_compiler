from __future__ import annotations

from typing import List

from .abstract_command import AbstractCommand
from ..abstract_syntax_tree import AbstractSyntaxTree
from ..visitor import Visitor


class CommandList(AbstractSyntaxTree):
    def __init__(self):
        self.commands: List[AbstractCommand] = []

    def visit(self, visitor: Visitor, *args) -> object:
        return visitor.visit_command_list(self)
