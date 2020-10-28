from .ast import AST
from .commands import CommandList
from .visitor import Visitor


class Program(AST):
    def __init__(self, command: CommandList):
        self.command = command

    def visit(self, v: Visitor):
        return v.visit_program(self)
