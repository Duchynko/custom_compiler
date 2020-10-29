from __future__ import annotations

from typing import List

from .expression_list import ExpressionList
from ..abstract_syntax_tree import AbstractSyntaxTree
from ..visitor import Visitor


class ArgumentsList(AbstractSyntaxTree):
    def __init__(self):
        self.expressions: List[ExpressionList] = []

    def visit(self, visitor: Visitor) -> object:
        return visitor.visit_arguments_list(self)
