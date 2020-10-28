from abstract_tree.visitor import Visitor
from .abstract_expression import AbstractExpression
from ..terminals.integer_literal import IntegerLiteral


class IntLiteralExpression(AbstractExpression):
    def __init__(self, literal: IntegerLiteral):
        self.literal = literal

    def visit(self, v: Visitor) -> object:
        return v.visit_int_literal_expression(self)
