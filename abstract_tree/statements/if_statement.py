from abstract_tree.visitor import Visitor
from .abstract_statement import AbstractStatement
from ..commands.commandlist import CommandList
from ..expressions.expression_list import ExpressionList


class IfStatement(AbstractStatement):
    def __init__(self, expr: ExpressionList, if_com: CommandList, else_com: CommandList):
        self.expr = expr
        self.if_com = if_com
        self.else_com = else_com

    def visit(self, v: Visitor) -> object:
        return v.visit_if_statement(self)
