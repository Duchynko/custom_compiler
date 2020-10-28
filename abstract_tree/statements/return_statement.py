from abstract_tree.visitor import Visitor
from .abstract_statement import AbstractStatement
from ..expressions.abstract_expression import AbstractExpression


class ReturnStatement(AbstractStatement):
    def __init__(self, expression: AbstractExpression):
        self.expression = expression

    def visit(self, v: Visitor) -> object:
        return v.visit_return_statement(self)
