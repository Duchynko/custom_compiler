from .abstract_statement import AbstractStatement
from ..expressions.expression_list import ExpressionList
from ..visitor import Visitor


class ExpressionStatement(AbstractStatement):
    def __init__(self, expressions: ExpressionList):
        self.expressions = expressions

    def visit(self, v: Visitor) -> object:
        return v.visit_expression_statement(self)
