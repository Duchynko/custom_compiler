from .single_expression import SingleExpression
from ..terminals.identifier import Identifier
from .expressions_list import ExpressionsList


class CallExpression(SingleExpression):
    def __init__(self, name: Identifier, args: ExpressionsList):
        self.name = name
        self.args = args
