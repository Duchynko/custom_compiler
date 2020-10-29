from __future__ import annotations

from typing import List

from .abstract_declaration import AbstractDeclaration
from ..abstract_syntax_tree import AbstractSyntaxTree
from ..visitor import Visitor


class DeclarationList(AbstractSyntaxTree):
    def __init__(self):
        self.declarations: List[AbstractDeclaration] = []

    def visit(self, visitor: Visitor) -> object:
        return visitor.visit_declaration_list(self)
