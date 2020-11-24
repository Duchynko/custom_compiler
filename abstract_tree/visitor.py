from __future__ import annotations

from abc import ABC, abstractmethod

from abstract_tree import *


class Visitor(ABC):
    @abstractmethod
    def visit_program(self, p: Program, *args) -> object:
        pass

    @abstractmethod
    def visit_command_list(self, c: CommandList, *args) -> object:
        pass

    @abstractmethod
    def visit_declaration_command(self, dc: DeclarationCommand, *args) -> object:
        pass

    @abstractmethod
    def visit_statement_command(self, sc: StatementCommand, *args) -> object:
        pass

    @abstractmethod
    def visit_declaration_list(self, d: DeclarationList, *args) -> object:
        pass

    @abstractmethod
    def visit_func_declaration(self, fd: FuncDeclaration, *args) -> object:
        pass

    @abstractmethod
    def visit_var_declaration(self, vd: VarDeclaration, *args) -> object:
        pass

    @abstractmethod
    def visit_var_declaration_with_assignment(self, vd: VarDeclarationWithAssignment, *args) -> object:
        pass

    @abstractmethod
    def visit_expression_statement(self, es: ExpressionStatement, *args) -> object:
        pass

    @abstractmethod
    def visit_if_statement(self, ifs: IfStatement, *args) -> object:
        pass

    @abstractmethod
    def visit_while_statement(self, ws: WhileStatement, *args) -> object:
        pass

    @abstractmethod
    def visit_expression_list(self, el: ExpressionList, *args) -> object:
        pass

    @abstractmethod
    def visit_binary_expression(self, be: BinaryExpression, *args) -> object:
        pass

    @abstractmethod
    def visit_return_statement(self, rs: ReturnStatement, *args) -> object:
        pass

    @abstractmethod
    def visit_call_expression(self, be: CallExpression, *args) -> object:
        pass

    @abstractmethod
    def visit_unary_expression(self, be: UnaryExpression, *args) -> object:
        pass

    @abstractmethod
    def visit_int_literal_expression(self, be: IntLiteralExpression, *args) -> object:
        pass

    @abstractmethod
    def visit_boolean_literal_expression(self, be: BooleanLiteralExpression, *args) -> object:
        pass

    @abstractmethod
    def visit_var_expression(self, be: VarExpression, *args) -> object:
        pass

    @abstractmethod
    def visit_arguments_list(self, al: ArgumentsList, *args) -> object:
        pass

    @abstractmethod
    def visit_identifier(self, i: Identifier, *args) -> object:
        pass

    @abstractmethod
    def visit_integer_literal(self, il: IntegerLiteral, *args) -> object:
        pass

    @abstractmethod
    def visit_boolean_literal(self, bl: BooleanLiteral, *args) -> object:
        pass

    @abstractmethod
    def visit_operator(self, o: Operator, *args) -> object:
        pass

    @abstractmethod
    def visit_type_indicator(self, td: TypeIndicator, *args) -> object:
        pass
