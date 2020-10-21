from ..ast import AST
from .single_declaration import SingleDeclaration


class Declaration(AST):
    def __init__(self):
        self.declarations: list(SingleDeclaration)
