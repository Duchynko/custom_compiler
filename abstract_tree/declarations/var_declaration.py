from ..ast import AST
from ..expressions.expression import Expression
from ..terminals.identifier import Identifier
from ..terminals.type_denoter import TypeDenoter
from ..terminals.operator import Operator
from .declaration import Declaration


class VarDeclaration(Declaration):
    def __init__(self, type_denoter: TypeDenoter, identifier: Identifier):
        self.identifier = identifier
        self.type_denoter = type_denoter


class VarDeclarationWithAssignment(Declaration):
    def __init__(self, type_denoter: TypeDenoter, identifier: Identifier, operator: Operator, expression: Expression):
        self.type_denoter = type_denoter
        self.identifier = identifier
        self.operator = operator
        self.expression = expression
