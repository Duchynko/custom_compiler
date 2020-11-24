from __future__ import annotations

from ..visitor import Visitor
from .abstract_expression import AbstractExpression
from .arguments_list import ArgumentsList
from ..terminals.identifier import Identifier


class CallExpression(AbstractExpression):
    def __init__(self, name: Identifier, args: ArgumentsList):
        self.name = name
        self.args = args

    def visit(self, visitor: Visitor, *args) -> object:
        return visitor.visit_call_expression(self, *args)
