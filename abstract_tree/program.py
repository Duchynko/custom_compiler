from .ast import AST
from .commands import Command


class Program(AST):
    def __init__(self, command: Command):
        self.command = command
