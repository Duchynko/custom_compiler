from typing import List

from .abstract_declaration import AbstractDeclaration
from ..ast import AST
from ..visitor import Visitor


class DeclarationList(AST):
    def __init__(self):
        self.declarations: List[AbstractDeclaration] = []

    def visit(self, v: Visitor) -> object:
        return v.visit_declaration_list(self)
