from __future__ import annotations

from ..visitor import Visitor
from ..expressions.abstract_expression import AbstractExpression
from .abstract_declaration import AbstractDeclaration
from ..terminals.identifier import Identifier
from ..terminals.operator import Operator
from ..terminals.type_indicator import TypeIndicator


class VarDeclaration(AbstractDeclaration):
    def __init__(self, type_indicator: TypeIndicator, identifier: Identifier):
        super().__init__()
        self.identifier = identifier
        self.type_indicator = type_indicator

    def visit(self, visitor: Visitor, *args) -> object:
        return visitor.visit_var_declaration(self, *args)


class VarDeclarationWithAssignment(AbstractDeclaration):
    def __init__(self, type_indicator: TypeIndicator, identifier: Identifier, operator: Operator,
                 expression: AbstractExpression):
        super().__init__()
        self.type_indicator = type_indicator
        self.identifier = identifier
        self.operator = operator
        self.expression = expression

    def visit(self, visitor: Visitor, *args) -> object:
        return visitor.visit_var_declaration_with_assignment(self, *args)


