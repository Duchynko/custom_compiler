from typing import List

from abstract_tree.visitor import Visitor
from ..ast import AST
from .expression_list import ExpressionList


class ArgumentsList(AST):
    def __init__(self):
        self.expressions: List[ExpressionList] = []

    def visit(self, v: Visitor) -> object:
        return v.visit_arguments_list(self)
