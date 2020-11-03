import unittest
from unittest import TestCase

from abstract_tree import BooleanLiteral, Identifier, IntegerLiteral, Operator, TypeIndicator, ArgumentsList, \
    VarExpression, UnaryExpression, IntLiteralExpression, VarDeclaration, BooleanLiteralExpression, BinaryExpression, \
    ExpressionList, VarDeclarationWithAssignment, DeclarationList, FuncDeclaration, CommandList, DeclarationCommand, \
    IfStatement
from checker import Checker
from exceptions import UndeclaredVariableException, InvalidOperatorException
from expression_type import ExpressionType


class TestChecker(TestCase):
    def setUp(self) -> None:
        self.c = Checker()

    def test_check(self):
        pass

    def test_visit_identifier(self):
        spelling = self.c.visit_identifier(Identifier("Hello"))
        self.assertEqual(spelling, "Hello")

    def test_visit_integer_literal(self):
        spelling = self.c.visit_integer_literal(IntegerLiteral("123"))
        self.assertEqual(spelling, "123")

    def test_visit_boolean_literal(self):
        spelling = self.c.visit_boolean_literal(BooleanLiteral("true"))
        self.assertEqual(spelling, "true")

    def test_visit_operator(self):
        spelling = self.c.visit_operator(Operator("~"))
        self.assertEqual(spelling, "~")

    def test_visit_type_indicator(self):
        spelling = self.c.visit_type_indicator(TypeIndicator("str"))
        self.assertEqual(spelling, "str")

    def test_visit_binary_expression(self):
        var_exp = VarExpression(Identifier("variable"))
        operator = Operator("+")
        un_exp = UnaryExpression(Operator("-"), IntLiteralExpression(IntegerLiteral("10")))
        var_dec = VarDeclaration(TypeIndicator("str"), Identifier("variable"))
        self.c.idTable.insert("variable", var_dec)

        exp_type: ExpressionType = self.c.visit_binary_expression(BinaryExpression(operator, var_exp, un_exp))

        self.assertTrue(exp_type.is_rvalue)

    def test_visit_binary_expression_invalid_left_side_of_the_expression(self):
        int_exp = IntLiteralExpression(IntegerLiteral("10"))
        operator = Operator("~")
        un_exp = UnaryExpression(Operator("-"), IntLiteralExpression(IntegerLiteral("10")))

        with self.assertRaises(Exception):
            self.c.visit_binary_expression(BinaryExpression(operator, int_exp, un_exp))

    def test_visit_call_expression(self):
        pass

    def test_visit_unary_expression(self):
        var_exp = VarExpression(Identifier("variable"))
        self.c.idTable.insert(var_exp.name.spelling, var_exp)
        un_exp = UnaryExpression(Operator("+"), var_exp)

        exp_type: ExpressionType = self.c.visit_unary_expression(un_exp)

        self.assertTrue(exp_type.is_rvalue)

    def test_visit_unary_expression_with_invalid_operator(self):
        var_exp = VarExpression(Identifier("variable"))
        self.c.idTable.insert(var_exp.name.spelling, var_exp)
        un_exp = UnaryExpression(Operator("~"), var_exp)

        with self.assertRaises(InvalidOperatorException):
            self.c.visit_unary_expression(un_exp)

    def test_visit_boolean_literal_expression(self):
        bool_lit = BooleanLiteral("true")

        exp_type: ExpressionType = self.c.visit_boolean_literal_expression(BooleanLiteralExpression(bool_lit))

        self.assertTrue(exp_type.is_rvalue)

    def test_visit_int_literal_expression(self):
        int_lit = IntegerLiteral("123")

        exp_type: ExpressionType = self.c.visit_int_literal_expression(IntLiteralExpression(int_lit))

        self.assertTrue(exp_type.is_rvalue)

    def test_visit_var_expression(self):
        identifier = Identifier("variable")
        var_type = TypeIndicator("str")
        self.c.idTable.insert(identifier=identifier.spelling, attr=VarDeclaration(var_type, identifier))

        exp_type: ExpressionType = self.c.visit_var_expression(VarExpression(identifier))

        self.assertFalse(exp_type.is_rvalue)

    def test_visit_var_expression_with_undeclared_variable(self):
        identifier = Identifier("variable")
        with self.assertRaises(UndeclaredVariableException):
            self.c.visit_var_expression(VarExpression(identifier))

    def test_visit_arguments_list(self):
        args = ArgumentsList()
        exp1 = IntLiteralExpression(IntegerLiteral("10"))
        exp2 = VarExpression(Identifier("variable"))
        args.expressions.extend([exp1, exp2])
        self.c.idTable.insert(
            identifier=exp2.name.spelling,
            attr=VarDeclaration(TypeIndicator("str"), Identifier(exp2.name.spelling))
        )

        exp_types = self.c.visit_arguments_list(args)

        self.assertEqual(len(exp_types), 2)

    def test_visit_expression_list_throws_on_undeclared_variable(self):
        el = ExpressionList()
        el.expressions.append(IntLiteralExpression(IntegerLiteral("10")))
        el.expressions.append(BooleanLiteralExpression(BooleanLiteral("true")))
        el.expressions.append(VarExpression(Identifier("number")))

        with self.assertRaises(UndeclaredVariableException):
            self.c.visit_expression_list(el)

    def test_visit_declaration_list(self):
        vd1 = VarDeclaration(TypeIndicator("str"), Identifier("name"))
        vd2 = VarDeclaration(TypeIndicator("int"), Identifier("age"))
        vd3 = VarDeclaration(TypeIndicator("bool"), Identifier("isAlive"))
        dl = DeclarationList()
        dl.declarations.extend([vd1, vd2, vd3])

        self.c.visit_declaration_list(dl)

        id_table = self.c.idTable.table
        self.assertEqual(id_table[0].attr, vd1)
        self.assertEqual(id_table[1].attr, vd2)
        self.assertEqual(id_table[2].attr, vd3)

    def test_visit_func_declaration(self):
        args = ArgumentsList()
        args.expressions.append(IntLiteralExpression(IntegerLiteral("10")))
        args.expressions.append(BooleanLiteralExpression(BooleanLiteral("true")))
        vd = VarDeclaration(TypeIndicator("str"), Identifier("variable"))
        dl = DeclarationList()
        dl.declarations.append(vd)
        block = CommandList()
        block.commands.append(DeclarationCommand(dl))
        fd = FuncDeclaration(
            identifier=Identifier("myFunc"),
            args=args,
            commands=block
        )

        self.c.visit_func_declaration(fd)

        id_entry = self.c.idTable.table[0]
        self.assertEqual(id_entry.attr, fd)

    def test_visit_var_declaration(self):
        vd = VarDeclaration(TypeIndicator("str"), Identifier("variable"))

        self.c.visit_var_declaration(vd)

        id_entry = self.c.idTable.table[0]
        self.assertEqual(id_entry.attr, vd)

    def test_visit_var_declaration_with_assignment(self):
        vda = VarDeclarationWithAssignment(
            type_indicator=TypeIndicator("str"),
            identifier=Identifier("variable"),
            operator=Operator("~"),
            expression=IntLiteralExpression(IntegerLiteral("10"))
        )

        self.c.visit_var_declaration_with_assignment(vda)

        id_entry = self.c.idTable.table[0]
        self.assertEqual(id_entry.attr, vda)

    def test_visit_program(self):
        pass

    def test_visit_command_list(self):
        pass

    def test_visit_declaration_command(self):
        pass

    def test_visit_statement_command(self):
        pass

    def test_visit_expression_statement(self):
        pass

    def test_visit_if_statement(self):
        pass

    def test_visit_while_statement(self):
        pass

    def test_visit_return_statement(self):
        pass


if __name__ == '__main__':
    unittest.main()
