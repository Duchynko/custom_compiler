from __future__ import annotations

from .abstract_declaration import AbstractDeclaration
from ..commands.commandlist import CommandList
from ..expressions.arguments_list import ArgumentsList
from ..terminals.identifier import Identifier
from ..visitor import Visitor


class FuncDeclaration(AbstractDeclaration):
    def __init__(self, identifier: Identifier, args: ArgumentsList, commands: CommandList):
        self.identifier = identifier
        self.args = args
        self.commands = commands

    def visit(self, visitor: Visitor) -> object:
        return visitor.visit_func_declaration(self)
