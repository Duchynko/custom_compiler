from typing import List

from ..ast import AST
from .abstract_command import AbstractCommand
from ..visitor import Visitor


class CommandList(AST):
    def __init__(self):
        self.commands: List[AbstractCommand] = []

    def visit(self, v: Visitor) -> object:
        return v.visit_command_list(self)
