from __future__ import annotations

from .abstract_declaration import AbstractDeclaration
from ..commands.commandlist import CommandList
from ..expressions.arguments_list import ArgumentsList
from ..terminals.identifier import Identifier
from ..visitor import Visitor


class FuncDeclaration(AbstractDeclaration):
    def __init__(self, identifier: Identifier, args: ArgumentsList, commands: CommandList):
        super().__init__()
        self.identifier = identifier
        self.args = args
        self.commands = commands

    def visit(self, visitor: Visitor, *args) -> object:
        return visitor.visit_func_declaration(self, *args)
