from ..ast import AST
from .single_command import SingleCommand
from ..declarations.declaration import Declaration


class DeclarationCommand(SingleCommand):
    def __init__(self, declaration: Declaration):
        self.declaration = declaration
