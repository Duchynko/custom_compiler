from ..ast import AST
from .single_command import SingleCommand


class Command(AST):
    def __init__(self):
        self.commands: list(SingleCommand)
