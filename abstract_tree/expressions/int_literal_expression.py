from .single_expression import SingleExpression
from ..terminals.integer_literal import IntegerLiteral


class IntLiteralExpression(SingleExpression):
    def __init__(self, literal: IntegerLiteral):
        self.literal = literal
