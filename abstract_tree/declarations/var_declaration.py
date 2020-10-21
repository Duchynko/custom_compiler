from ..ast import AST
from ..expressions.expression import Expression
from ..terminals.identifier import Identifier
from .declaration import Declaration


class VarDeclaration(Declaration):
    def __init__(self, type_denoter: TypeDenoter, identifier: Identifier, expression: Expression):
        self.identifier = identifier
        self.expression = expression
        self.type_denoter = type_denoter
