from abstract_tree.visitor import Visitor
from .abstract_expression import AbstractExpression
from ..terminals.identifier import Identifier


class VarExpression(AbstractExpression):
    def __init__(self, name: Identifier):
        self.name = name

    def visit(self, v: Visitor) -> object:
        return v.visit_var_expression(self)
