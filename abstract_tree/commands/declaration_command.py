from .abstract_command import AbstractCommand
from ..declarations.declarationlist import DeclarationList
from ..visitor import Visitor


class DeclarationCommand(AbstractCommand):
    def __init__(self, declaration: DeclarationList):
        self.declaration = declaration

    def visit(self, v: Visitor) -> object:
        return v.visit_declaration_command(self)
