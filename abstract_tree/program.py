from ast import AST
from command import Command


class Program(AST):
    def __init__(self, command: Command):
        self.command = command
