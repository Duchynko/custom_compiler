from .abstract_expression import AbstractExpression
from ..terminals.identifier import Identifier
from .arguments_list import ArgumentsList
from ..visitor import Visitor


class CallExpression(AbstractExpression):
    def __init__(self, name: Identifier, args: ArgumentsList):
        self.name = name
        self.args = args

    def visit(self, v: Visitor) -> object:
        return v.visit_call_expression(self)
