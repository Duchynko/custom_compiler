from typing import List

# from abstract_tree.commands import CommandList, DeclarationCommand, StatementCommand
# from abstract_tree.declarations import DeclarationList, FuncDeclaration, VarDeclaration, VarDeclarationWithAssignment
# from abstract_tree.expressions import BinaryExpression, CallExpression, UnaryExpression, BooleanLiteralExpression, \
#     IntLiteralExpression, VarExpression, ArgumentsList
# from abstract_tree.expressions.expression_list import ExpressionList
# from abstract_tree.program import Program
# from abstract_tree.statements import IfStatement, ExpressionStatement, WhileStatement, ReturnStatement
# from abstract_tree.terminals import BooleanLiteral, Identifier, IntegerLiteral, Operator, TypeIndicator
from abstract_tree.visitor import Visitor
from abstract_tree import *
from exceptions import UndeclaredVariableException, InvalidOperatorException
from expression_type import ExpressionType
from identification_table import IdentificationTable
from tokens import ADDOPS, MULOPS, ASSIGNOPS


class Checker(Visitor):
    def __init__(self):
        self.idTable = IdentificationTable()

    def check(self, p: Program):
        p.visit(self)

    def visit_binary_expression(self, be: BinaryExpression, *args) -> ExpressionType:
        t1: ExpressionType = be.expression1.visit(self)
        _: ExpressionType = be.expression2.visit(self)
        operator = be.operator.visit(self)

        if operator in ASSIGNOPS and t1.is_rvalue:
            raise Exception("Left-hand side of the expression must be a variable.")

        return ExpressionType(True)

    def visit_call_expression(self, ce: CallExpression, *args):
        func_name: str = ce.name.visit(self)
        types: List[ExpressionType] = ce.args.visit(self)
        declaration = self.idTable.get(func_name)

        if not declaration:
            raise Exception(f"Function {func_name} is not declared.")

        if isinstance(declaration, FuncDeclaration):
            fd: FuncDeclaration = declaration
            ce.declaration = fd
            if len(types) != len(fd.args.expressions):
                raise Exception(f"Function {func_name} expects {len(fd.args.expressions)} number of arguments.")
        else:
            raise Exception(f"{func_name} is not callable.")

        return ExpressionType(False)

    def visit_unary_expression(self, ue: UnaryExpression, *args) -> ExpressionType:
        ue.expression.visit(self)
        operator = ue.operator.visit(self)

        if operator not in ADDOPS + MULOPS:
            raise InvalidOperatorException(f"Operator {operator} is not allowed here.")
        return ExpressionType(True)

    def visit_boolean_literal_expression(self, be: BooleanLiteralExpression, *args) -> ExpressionType:
        be.literal.visit(self)
        return ExpressionType(True)

    def visit_int_literal_expression(self, ie: IntLiteralExpression, *args) -> ExpressionType:
        ie.literal.visit(self)
        return ExpressionType(True)

    def visit_var_expression(self, ve: VarExpression, *args) -> ExpressionType:
        identifier: str = ve.name.visit(self)
        declaration = self.idTable.get(identifier)

        if declaration:
            ve.declaration = declaration
            return ExpressionType(False)
        else:
            raise UndeclaredVariableException(f"Variable {identifier} is not defined.")

    def visit_arguments_list(self, al: ArgumentsList, *args) -> List[ExpressionType]:
        types: List[ExpressionType] = []

        for a in al.expressions:
            types.append(a.visit(self))

        return types

    def visit_expression_list(self, el: ExpressionList, *args) -> None:
        for expression in el.expressions:
            expression.visit(self)
        return None

    def visit_program(self, p: Program, *args) -> object:
        self.idTable.openScope()
        p.command_list.visit(self)
        self.idTable.closeScope()
        return None

    def visit_command_list(self, c: CommandList, *args) -> object:
        for command in c.commands:
            command.visit(self)
        return None

    def visit_declaration_command(self, dc: DeclarationCommand, *args) -> object:
        for declaration in dc.declaration_list.declarations:
            declaration.visit(self, )
        return None

    def visit_statement_command(self, sc: StatementCommand, *args) -> object:
        sc.statement.visit(self)
        return None

    def visit_declaration_list(self, d: DeclarationList, *args) -> object:
        for declaration in d.declarations:
            declaration.visit(self, )
        return None

    def visit_func_declaration(self, fd: FuncDeclaration, *args) -> object:
        identifier = fd.identifier.visit(self)

        self.idTable.insert(identifier=identifier, attr=fd)
        self.idTable.openScope()

        fd.commands.visit(self)
        fd.args.visit(self)

        self.idTable.closeScope()
        return None

    def visit_var_declaration(self, vd: VarDeclaration, *args) -> None:
        identifier: str = vd.identifier.visit(self)

        self.idTable.insert(identifier=identifier, attr=vd)
        return None

    def visit_var_declaration_with_assignment(self, vd: VarDeclarationWithAssignment, *args) -> object:
        identifier: str = vd.identifier.visit(self)

        self.idTable.insert(identifier, vd)
        return None

    def visit_expression_statement(self, es: ExpressionStatement, *args) -> object:
        es.expressions.visit(self)
        return None

    def visit_if_statement(self, ifs: IfStatement, *args) -> object:
        ifs.expr.visit(self)
        ifs.if_com.visit(self)
        ifs.else_com.visit(self)
        return None

    def visit_while_statement(self, ws: WhileStatement, *args) -> object:
        ws.expr.visit(self)
        ws.command.visit(self)
        return None

    def visit_return_statement(self, rs: ReturnStatement, *args) -> object:
        rs.expression.visit(self)
        return None

    def visit_identifier(self, i: Identifier, *args) -> object:
        return i.spelling

    def visit_integer_literal(self, il: IntegerLiteral, *args) -> object:
        return il.spelling

    def visit_boolean_literal(self, bl: BooleanLiteral, *args) -> object:
        return bl.spelling

    def visit_operator(self, o: Operator, *args) -> object:
        return o.spelling

    def visit_type_indicator(self, td: TypeIndicator, *args) -> object:
        return td.spelling
