from .single_expression import SingleExpression
from ..terminals.identifier import Identifier


class VarExpression(SingleExpression):
    def __init__(self, name: Identifier):
        self.name = name
