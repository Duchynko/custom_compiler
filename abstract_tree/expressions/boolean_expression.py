from abstract_tree.visitor import Visitor
from .abstract_expression import AbstractExpression
from ..terminals.boolean_literal import BooleanLiteral


class BooleanLiteralExpression(AbstractExpression):
    def __init__(self, literal: BooleanLiteral):
        self.literal = literal

    def visit(self, v: Visitor) -> object:
        return v.visit_boolean_literal_expression(self)
