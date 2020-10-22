from .single_statement import SingleStatement
from ..expressions.single_expression import SingleExpression


class ReturnStatement(SingleStatement):
    def __init__(self, expression: SingleExpression):
        self.expression = expression
