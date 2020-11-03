from __future__ import annotations

from typing import List

from .abstract_expression import AbstractExpression
from ..abstract_syntax_tree import AbstractSyntaxTree
from ..visitor import Visitor


class ArgumentsList(AbstractSyntaxTree):
    def __init__(self):
        self.expressions: List[AbstractExpression] = []

    def visit(self, visitor: Visitor) -> object:
        return visitor.visit_arguments_list(self)
