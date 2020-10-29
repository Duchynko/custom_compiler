from __future__ import annotations

from typing import List

from ..visitor import Visitor
from .abstract_expression import AbstractExpression
from ..abstract_syntax_tree import AbstractSyntaxTree


class ExpressionList(AbstractSyntaxTree):
    def __init__(self):
        self.expressions = List[AbstractExpression]()

    def visit(self, visitor: Visitor) -> object:
        return visitor.visit_expression_list(self)

