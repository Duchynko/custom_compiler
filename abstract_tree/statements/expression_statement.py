from ..ast import AST
from .single_statement import SingleStatement
from ..commands.command import Command
from ..expressions.expression import Expression


class ExpressionStatement(SingleStatement):
    def __init__(self, expressions: Expression):
        self.expressions = expressions
