from abstract_tree import AbstractDeclaration
from ..expressions.expression_list import ExpressionList
from ..terminals.identifier import Identifier
from ..terminals.operator import Operator
from ..terminals.type_indicator import TypeIndicator
from ..visitor import Visitor


class VarDeclaration(AbstractDeclaration):
    def __init__(self, type_indicator: TypeIndicator, identifier: Identifier):
        self.identifier = identifier
        self.type_indicator = type_indicator

    def visit(self, v: Visitor) -> object:
        return v.visit_var_declaration(self)


class VarDeclarationWithAssignment(AbstractDeclaration):
    def __init__(self, type_indicator: TypeIndicator, identifier: Identifier, operator: Operator, expression: ExpressionList):
        self.type_indicator = type_indicator
        self.identifier = identifier
        self.operator = operator
        self.expression = expression

    def visit(self, v: Visitor) -> object:
        return v.visit_var_declaration_with_assignment(self)
