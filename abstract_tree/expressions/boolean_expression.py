from .single_expression import SingleExpression
from ..terminals.boolean_literal import BooleanLiteral


class BooleanLiteralExpression(SingleExpression):
    def __init__(self, literal: BooleanLiteral):
        self.literal = literal
