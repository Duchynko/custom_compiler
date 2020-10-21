from ..ast import AST
from .single_statement import SingleStatement
from ..commands.command import Command
from ..expressions.expression import Expression


class IfStatement(SingleStatement):
    def __init__(self, expr: Expression, ifCom: Command, elseCom: Command):
        self.expr = expr
        self.ifCom = ifCom
        self.elseCom = elseCom
