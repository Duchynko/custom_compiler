from .declaration import Declaration
from ..expressions.expressions_list import ExpressionsList
from ..commands.command import Command
from ..terminals.identifier import Identifier


class FuncDeclaration(Declaration):
    def __init__(self, identifier: Identifier, args: ExpressionsList, commands: Command):
        self.identifier = identifier
        self.args = args
        self.commands = commands
