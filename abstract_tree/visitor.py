from abc import ABC, abstractmethod

from abstract_tree.expressions.expression_list import ExpressionList
from .program import Program
from .commands import CommandList, DeclarationCommand, StatementCommand
from .declarations import (DeclarationList, FuncDeclaration, VarDeclaration,
                           VarDeclarationWithAssignment)
from .statements import (IfStatement, ExpressionStatement, WhileStatement,
                         ReturnStatement)
from .terminals import (BooleanLiteral, Identifier, IntegerLiteral,
                        Operator, TypeIndicator)
from .expressions import (BinaryExpression, UnaryExpression, CallExpression,
                          BooleanLiteralExpression, IntLiteralExpression,
                          ArgumentsList, VarExpression)


class Visitor(ABC):

    @abstractmethod
    def visit_program(self, p: Program) -> object:
        pass

    @abstractmethod
    def visit_command_list(self, c: CommandList) -> object:
        pass

    @abstractmethod
    def visit_declaration_command(self, dc: DeclarationCommand) -> object:
        pass

    @abstractmethod
    def visit_statement_command(self, sc: StatementCommand) -> object:
        pass

    @abstractmethod
    def visit_declaration_list(self, d: DeclarationList) -> object:
        pass

    @abstractmethod
    def visit_func_declaration(self, fd: FuncDeclaration) -> object:
        pass

    @abstractmethod
    def visit_var_declaration(self, vd: VarDeclaration) -> object:
        pass

    @abstractmethod
    def visit_var_declaration_with_assignment(self, vd: VarDeclarationWithAssignment) -> object:
        pass

    @abstractmethod
    def visit_expression_statement(self, es: ExpressionStatement) -> object:
        pass

    @abstractmethod
    def visit_if_statement(self, ifs: IfStatement) -> object:
        pass

    @abstractmethod
    def visit_while_statement(self, ws: WhileStatement) -> object:
        pass

    @abstractmethod
    def visit_expression_list(self, el: ExpressionList) -> object:
        pass

    @abstractmethod
    def visit_binary_expression(self, be: BinaryExpression) -> object:
        pass

    @abstractmethod
    def visit_return_statement(self, rs: ReturnStatement) -> object:
        pass

    @abstractmethod
    def visit_call_expression(self, be: CallExpression) -> object:
        pass

    @abstractmethod
    def visit_unary_expression(self, be: UnaryExpression) -> object:
        pass

    @abstractmethod
    def visit_int_literal_expression(self, be: IntLiteralExpression) -> object:
        pass

    @abstractmethod
    def visit_boolean_literal_expression(self, be: BooleanLiteralExpression) -> object:
        pass

    @abstractmethod
    def visit_var_expression(self, be: VarExpression) -> object:
        pass

    @abstractmethod
    def visit_arguments_list(self, al: ArgumentsList) -> object:
        pass

    @abstractmethod
    def visit_identifier(self, i: Identifier) -> object:
        pass

    @abstractmethod
    def visit_integer_literal(self, il: IntegerLiteral) -> object:
        pass

    @abstractmethod
    def visit_boolean_literal(self, bl: BooleanLiteral) -> object:
        pass

    @abstractmethod
    def visit_operator(self, o: Operator) -> object:
        pass

    @abstractmethod
    def visit_type_indicator(self, td: TypeIndicator) -> object:
        pass
