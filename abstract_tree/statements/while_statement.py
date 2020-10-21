from ..ast import AST
from ..commands.command import Command
from .single_statement import SingleStatement
from ..expressions.expression import Expression


class WhileStatement(SingleStatement):
    def __init__(self, expr: Expression, command: Command):
        self.command = command
        self.expr = expr
