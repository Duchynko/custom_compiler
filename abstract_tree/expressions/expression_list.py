from typing import List

from abstract_tree.visitor import Visitor
from ..ast import AST
from .abstract_expression import AbstractExpression


class ExpressionList(AST):
    def __init__(self):
        self.expressions: List[AbstractExpression]

    def visit(self, v: Visitor) -> object:
        return v.visit_expression_list(self)

