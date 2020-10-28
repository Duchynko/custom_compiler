import unittest
from unittest.mock import patch, mock_open
from scanner import Scanner, SourceFile
from parser import Parser
from tokens import Kind, TYPE_DENOTERS
from exceptions import UnsupportedExpressionTokenException
from abstract_tree import (TypeIndicator, IntLiteralExpression, VarExpression,
                           UnaryExpression, VarDeclarationWithAssignment,
                           FuncDeclaration, VarDeclaration, StatementCommand,
                           DeclarationCommand, CommandList, Program,
                           BinaryExpression)
import json
from itertools import chain


class TestParser(unittest.TestCase):
    def test_init_one(self):
        with patch('builtins.open', mock_open(read_data='Hello')):
            s = Scanner('file')
            p = Parser(s)

            self.assertEqual(p.current_terminal.kind,
                             Kind.IDENTIFIER)

    def test_accept_one_true(self):
        with patch('builtins.open', mock_open(read_data='Hello')):
            s = Scanner('file')
            p = Parser(s)

            self.assertTrue(p.accept(Kind.IDENTIFIER))

    # def test_accept_one_false(self):
    #     with patch('builtins.open', mock_open(read_data='Hello')):
    #         s = Scanner('file')
    #         p = Parser(s)

    #         self.assertFalse(p.accept(Kind.OPERATOR))

    def test_accept_multiple_true(self):
        with patch('builtins.open', mock_open(read_data='if Hello ==')):
            s = Scanner('file')
            p = Parser(s)

            self.assertTrue(p.accept(Kind.IF))
            self.assertTrue(p.accept(Kind.IDENTIFIER))
            self.assertTrue(p.accept(Kind.OPERATOR))

    def test_parse_type_denoter(self):
        with patch('builtins.open', mock_open(read_data="int")):
            s = Scanner('file')
            p = Parser(s)

            type_d = p.parse_type_denoter()

            self.assertTrue(isinstance(type_d, TypeIndicator))
            self.assertEqual(type_d.spelling, 'int')
            self.assertEqual(p.current_terminal.kind,
                             Kind.EOT)

    ######################
    # Signle-Expressions #
    ######################

    def test_parse_single_int_literal_expression(self):
        with patch('builtins.open', mock_open(read_data='123')):
            s = Scanner('file')
            p = Parser(s)

            expression = p.parse_single_expression()

            self.assertTrue(isinstance(expression, IntLiteralExpression))
            self.assertEqual(expression.literal.spelling, '123')
            self.assertEqual(p.current_terminal.kind, Kind.EOT)

    def test_parse_single_var_expression(self):
        with patch('builtins.open', mock_open(read_data='hello')):
            s = Scanner('file')
            p = Parser(s)

            expression = p.parse_single_expression()

            self.assertTrue(isinstance(expression, VarExpression))
            self.assertEqual(expression.name.spelling, 'hello')
            self.assertEqual(p.current_terminal.kind, Kind.EOT)

    def test_parse_single_unary_expression(self):
        with patch('builtins.open', mock_open(read_data='+1')):
            s = Scanner('file')
            p = Parser(s)

            expression = p.parse_single_expression()

            self.assertTrue(isinstance(expression, UnaryExpression))
            self.assertEqual(expression.operator.spelling, '+')
            self.assertEqual(expression.expression.literal.spelling, '1')
            self.assertEqual(p.current_terminal.kind, Kind.EOT)

    def test_parse_single_unary_expression_with_recursive_unary_expression(self):
        with patch('builtins.open', mock_open(read_data='+-30')):
            s = Scanner('file')
            p = Parser(s)

            expression = p.parse_single_expression()

            self.assertTrue(isinstance(expression, UnaryExpression))
            self.assertTrue(isinstance(expression.expression, UnaryExpression))
            self.assertEqual(p.current_terminal.kind, Kind.EOT)

    def test_parse_single_expression_raises_when_unexpected_token(self):
        with patch('builtins.open', mock_open(read_data='(Hello)')):
            s = Scanner('file')
            p = Parser(s)

            with self.assertRaises(UnsupportedExpressionTokenException):
                p.parse_single_expression()

    ###############
    # Expressions #
    ###############

    def test_parse_expression_var_expression(self):
        with patch('builtins.open', mock_open(read_data='hello')):
            s = Scanner('file')
            p = Parser(s)

            expression = p.parse_expression()

            self.assertTrue(isinstance(expression, VarExpression))
            self.assertEqual(expression.name.spelling, 'hello')
            self.assertEqual(p.current_terminal.kind, Kind.EOT)

    def test_parse_expression_nested_binary_expressions_with_int_literal_expression(self):
        with patch('builtins.open', mock_open(read_data='5+4+3')):
            s = Scanner('file')
            p = Parser(s)

            expression = p.parse_expression()

            self.assertTrue(isinstance(expression, BinaryExpression))
            self.assertTrue(isinstance(
                expression.expression1, BinaryExpression))
            self.assertTrue(isinstance(
                expression.expression2, IntLiteralExpression))
            self.assertEqual(p.current_terminal.kind, Kind.EOT)

    def test_parse_expression_binary_expressions(self):
        with patch('builtins.open', mock_open(read_data='5+five')):
            s = Scanner('file')
            p = Parser(s)

            expression = p.parse_expression()

            self.assertTrue(isinstance(expression, BinaryExpression))
            self.assertEqual(p.current_terminal.kind,
                             Kind.EOT)

    def test_parse_expression_nested_binary_expressions_with_unary_expression(self):
        with patch('builtins.open', mock_open(read_data='5+five+-10')):
            s = Scanner('file')
            p = Parser(s)

            expression = p.parse_expression()

            self.assertTrue(isinstance(expression, BinaryExpression))
            self.assertTrue(isinstance(
                expression.expression1, BinaryExpression))
            self.assertTrue(isinstance(
                expression.expression2, UnaryExpression))
            self.assertEqual(p.current_terminal.kind,
                             Kind.EOT)

    #######################
    # Signle declarations #
    #######################

    def test_parse_single_var_declaration(self):
        with patch('builtins.open', mock_open(read_data='int five ~ 5')):
            s = Scanner('file')
            p = Parser(s)

            var_declaration = p.parse_single_declaration()

            self.assertTrue(isinstance(
                var_declaration, VarDeclarationWithAssignment))
            self.assertEqual(p.current_terminal.kind,
                             Kind.EOT)

    def test_parse_single_var_declaration_with_asignment(self):
        with patch('builtins.open', mock_open(read_data='int five ~ 5+five-10')):
            s = Scanner('file')
            p = Parser(s)

            declaration = p.parse_single_declaration()

            self.assertTrue(isinstance(
                declaration, VarDeclarationWithAssignment))
            self.assertTrue(isinstance(
                declaration.expression, BinaryExpression))
            self.assertEqual(p.current_terminal.kind,
                             Kind.EOT)

    def test_parse_single_func_declaration_with_one_argument(self):
        input = """
        func helloworld(arg):
            int arg ~ 10;
            str hello ~ world;
            str joined ~ arg + hello;
        end
        """
        with patch('builtins.open', mock_open(read_data=input)):
            s = Scanner('file')
            p = Parser(s)

            func_declaration: FuncDeclaration = p.parse_single_declaration()
            args_length = len(func_declaration.args.expressions)

            self.assertTrue(isinstance(func_declaration, FuncDeclaration))
            self.assertEquals(args_length, 1)
            self.assertEqual(p.current_terminal.kind, Kind.EOT)

    def test_parse_single_func_declaration_with_multiple_arguments(self):
        input = """
        func helloworld(arg, org, erg):
            int arg ~ 10;
            str org ~ world;
            str joined ~ arg + org;
        end
        """
        with patch('builtins.open', mock_open(read_data=input)):
            s = Scanner('file')
            p = Parser(s)

            func_declaration: FuncDeclaration = p.parse_single_declaration()
            args_length = len(func_declaration.args.expressions)

            self.assertTrue(isinstance(func_declaration, FuncDeclaration))
            self.assertEquals(args_length, 3)
            self.assertEqual(p.current_terminal.kind, Kind.EOT)

    # TODO: Add tests with return statements

    ################
    # Declarations #
    ################

    def test_parse_declarations_multiple_var_declarations(self):
        input_text = """
        int five ~ 5
        str dog ~ wuf
        """
        with patch('builtins.open', mock_open(read_data=input_text)):
            s = Scanner('file')
            p = Parser(s)

            declaration = p.parse_declaration()
            var_declarations = [
                var_declaration for var_declaration in declaration.declarations]

            self.assertTrue(all(isinstance(d, VarDeclarationWithAssignment)
                                for d in var_declarations))
            self.assertTrue(len(var_declarations), 2)
            self.assertEqual(p.current_terminal.kind,
                             Kind.EOT)

    def test_parse_declaration_var_and_func_declarations_with_while_statement(self):
        input_text = """
        int five ~ 5
        func helloworld(count):
            int six ~ 6;
            while (six):
                count ~ count+1;
            end
        end
        """
        with patch('builtins.open', mock_open(read_data=input_text)):
            s = Scanner('file')
            p = Parser(s)

            declarations = p.parse_declaration()
            var_declaration = declarations.declarations[0]
            func_declaration = declarations.declarations[1]

            self.assertTrue(isinstance(var_declaration,
                                       VarDeclarationWithAssignment))
            self.assertTrue(isinstance(func_declaration, FuncDeclaration))
            self.assertEqual(p.current_terminal.kind,
                             Kind.EOT)

    def test_parse_declaration_var_and_func_declarations(self):
        input_text = """
        int five ~ 5
        func helloworld(count):
            int six ~ 6;
            count ~ count+1;
        end
        """
        with patch('builtins.open', mock_open(read_data=input_text)):
            s = Scanner('file')
            p = Parser(s)

            declarations = p.parse_declaration()
            var_declaration = declarations.declarations[0]
            func_declaration = declarations.declarations[1]

            self.assertTrue(isinstance(var_declaration,
                                       VarDeclarationWithAssignment))
            self.assertTrue(isinstance(func_declaration, FuncDeclaration))
            self.assertEqual(p.current_terminal.kind,
                             Kind.EOT)

    def test_parse_declaration_multiple_fun_declarations(self):
        input_text = """
        func helloworld(count):
            int six ~ 6;
            count ~ count+1;
        end

        func helloWorld(ten, four):
            int six ~ 6;
            six ~ six + 1;
        end
        """
        with patch('builtins.open', mock_open(read_data=input_text)):
            s = Scanner('file')
            p = Parser(s)

            declarations = p.parse_declaration()

            self.assertTrue(isinstance(
                declarations.declarations[0], FuncDeclaration))
            self.assertTrue(isinstance(
                declarations.declarations[1], FuncDeclaration))
            self.assertEqual(p.current_terminal.kind,
                             Kind.EOT)

    ###################
    # Single-commands #
    ###################

    def test_parse_single_command_statement_command(self):
        with patch('builtins.open', mock_open(read_data='helloworld(123);')):
            s = Scanner('file')
            p = Parser(s)

            command = p.parse_single_command()

            self.assertTrue(isinstance(command, StatementCommand))
            self.assertEqual(
                p.current_terminal.kind, Kind.EOT)

    def test_parse_single_command_statement_command_2(self):
        with patch('builtins.open', mock_open(read_data='helloworld(123, hello, world);')):
            s = Scanner('file')
            p = Parser(s)

            command = p.parse_single_command()

            self.assertTrue(isinstance(command, StatementCommand))
            self.assertEqual(
                p.current_terminal.kind, Kind.EOT)

    def test_parse_single_command_declaration_command(self):
        input_text = """
        func helloworld(count):
            int six ~ 6;
            count ~ count+1;
        end
        """
        with patch('builtins.open', mock_open(read_data=input_text)):
            s = Scanner('file')
            p = Parser(s)

            command = p.parse_single_command()

            self.assertTrue(isinstance(command, DeclarationCommand))
            self.assertEqual(
                p.current_terminal.kind, Kind.EOT)

    ############
    # Commands #
    ############

    def test_parse_command_multiple_statement_commands(self):
        with patch('builtins.open', mock_open(read_data='helloworld(arg); helloworld2(); helloworld3(arg1, arg2);')):
            s = Scanner('file')
            p = Parser(s)

            command = p.parse_command()

            self.assertTrue(isinstance(command, CommandList))
            self.assertTrue(all(isinstance(c, StatementCommand)
                                for c in command.commands))
            self.assertEqual(
                p.current_terminal.kind, Kind.EOT)

    def test_parse_command_multiple_declaration_commands(self):
        with patch('builtins.open', mock_open(read_data='int one; int two ~ 2;')):
            s = Scanner('file')
            p = Parser(s)

            command = p.parse_command()

            self.assertTrue(isinstance(command, CommandList))
            self.assertTrue(all(isinstance(c, DeclarationCommand)
                                for c in command.commands))
            self.assertEqual(
                p.current_terminal.kind, Kind.EOT)

    ###########
    # Program #
    ###########

    def test_parse_program(self):
        input_text = """
        int ten ~ 10;

        func helloWorld(ten, four):
            int six ~ 6;
            six ~ six + 1;
        end

        if (ten == 11):
            int seven ~ 7;
            return True
        else:
            return False
        end
        """

        with patch('builtins.open', mock_open(read_data=input_text)):
            s = Scanner('file')
            p = Parser(s)

            program = p.parse_program()

            self.assertTrue(isinstance(program, Program))
            self.assertEqual(p.current_terminal.kind,
                             Kind.EOT)
