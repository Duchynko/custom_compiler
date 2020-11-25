from __future__ import annotations

from .abstract_command import AbstractCommand
from ..declarations.declarationlist import DeclarationList
from ..visitor import Visitor


class DeclarationCommand(AbstractCommand):
    def __init__(self, declaration_list: DeclarationList):
        self.declaration_list = declaration_list

    def visit(self, visitor: Visitor, *args) -> object:
        return visitor.visit_declaration_command(self, *args)
