from abstract_tree.visitor import Visitor
from .abstract_statement import AbstractStatement
from ..commands.commandlist import CommandList
from ..expressions.expression_list import ExpressionList


class WhileStatement(AbstractStatement):
    def __init__(self, expr: ExpressionList, command: CommandList):
        self.command = command
        self.expr = expr

    def visit(self, v: Visitor) -> object:
        return v.visit_while_statement(self)
