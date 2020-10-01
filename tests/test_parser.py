import unittest
from unittest.mock import patch, mock_open
from scanner import Scanner, SourceFile
from parser import Parser
from tokens import TokenType


class TestParser(unittest.TestCase):
    def test_init_one(self):
        with patch('builtins.open', mock_open(read_data='Hello')):
            s = Scanner('file')
            p = Parser(s)

            self.assertEqual(p.current_terminal.tokenType,
                             TokenType.IDENTIFIER)

    def test_accept_one_true(self):
        with patch('builtins.open', mock_open(read_data='Hello')):
            s = Scanner('file')
            p = Parser(s)

            self.assertTrue(p.accept(TokenType.IDENTIFIER))

    def test_accept_one_false(self):
        with patch('builtins.open', mock_open(read_data='Hello')):
            s = Scanner('file')
            p = Parser(s)

            self.assertFalse(p.accept(TokenType.OPERATOR))

    def test_accept_multiple_true(self):
        with patch('builtins.open', mock_open(read_data='if Hello ==')):
            s = Scanner('file')
            p = Parser(s)

            self.assertTrue(p.accept(TokenType.IF))
            self.assertTrue(p.accept(TokenType.IDENTIFIER))
            self.assertTrue(p.accept(TokenType.OPERATOR))

    def test_parse_single_expression_starts_with_integer_literal(self):
        with patch('builtins.open', mock_open(read_data='123 Hello')):
            s = Scanner('file')
            p = Parser(s)

            assert(p.current_terminal.tokenType is TokenType.INTEGER_LITERAL)
            p.parse_single_expression()

            self.assertEqual(
                p.current_terminal.tokenType, TokenType.IDENTIFIER)

    def test_parse_single_expression_starts_with_identifier(self):
        with patch('builtins.open', mock_open(read_data='Hello 123')):
            s = Scanner('file')
            p = Parser(s)

            assert(p.current_terminal.tokenType is TokenType.IDENTIFIER)
            p.parse_single_expression()

            self.assertEqual(
                p.current_terminal.tokenType, TokenType.INTEGER_LITERAL)

    # def test_parse_single_expression_starts_with_boolean_literal(self):
    #     with patch('builtins.open', mock_open(read_data='True;')):
    #         s = Scanner('file')
    #         p = Parser(s)

    #         assert(p.current_terminal.tokenType is TokenType.INTEGER_LITERAL)
    #         p.parse_single_expression()

    #         self.assertEqual(
    #             p.current_terminal.tokenType, TokenType.IDENTIFIER)

    def test_parse_single_expression_starts_with_operator_followed_by_single_expression(self):
        with patch('builtins.open', mock_open(read_data='+1 Hello')):
            s = Scanner('file')
            p = Parser(s)

            assert(p.current_terminal.tokenType is TokenType.OPERATOR)
            p.parse_single_expression()

            self.assertEqual(
                p.current_terminal.tokenType, TokenType.IDENTIFIER)

    def test_parse_single_expression_starts_with_operator_recursion_followed_by_single_expression(self):
        with patch('builtins.open', mock_open(read_data='+-30 Hello')):
            s = Scanner('file')
            p = Parser(s)

            assert(p.current_terminal.spelling is '+')
            p.parse_single_expression()

            self.assertEqual(
                p.current_terminal.tokenType, TokenType.IDENTIFIER)

    def test_parse_single_expression_raises_when_unexpected_token(self):
        with patch('builtins.open', mock_open(read_data='(Hello)')):
            s = Scanner('file')
            p = Parser(s)

            assert(p.current_terminal.spelling is '(')

            with self.assertRaises(Exception):
                p.parse_single_expression()

    def test_parse_expression_single_expression(self):
        with patch('builtins.open', mock_open(read_data='Hello ;')):
            s = Scanner('file')
            p = Parser(s)

            assert(p.current_terminal.tokenType is TokenType.IDENTIFIER)
            p.parse_expression()

            self.assertEqual(p.current_terminal.tokenType,
                             TokenType.SEMICOLON)

    def test_parse_expression_multiple_operator_and_integers(self):
        with patch('builtins.open', mock_open(read_data='5+4+3 ;')):
            s = Scanner('file')
            p = Parser(s)

            assert(p.current_terminal.spelling is '5')
            p.parse_expression()

            self.assertEqual(p.current_terminal.tokenType,
                             TokenType.SEMICOLON)

    def test_parse_expression_multiple_operator_integer_and_string(self):
        with patch('builtins.open', mock_open(read_data='5+five ;')):
            s = Scanner('file')
            p = Parser(s)

            assert(p.current_terminal.spelling is '5')
            p.parse_expression()

            self.assertEqual(p.current_terminal.tokenType,
                             TokenType.SEMICOLON)

    def test_parse_expression_multiple_integer_identifier_operator(self):
        with patch('builtins.open', mock_open(read_data='5+five+-10;')):
            s = Scanner('file')
            p = Parser(s)

            p.parse_expression()

            self.assertEqual(p.current_terminal.tokenType,
                             TokenType.SEMICOLON)

    def test_parse_single_declaration_variable(self):
        with patch('builtins.open', mock_open(read_data='int five ~ 5;')):
            s = Scanner('file')
            p = Parser(s)

            assert(p.current_terminal.spelling == 'int')
            p.parse_single_declaration()

            self.assertEqual(p.current_terminal.tokenType,
                             TokenType.EOT)

    def test_parse_single_declaration_function_with_one_argument(self):
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

            p.parse_single_declaration()

            self.assertEqual(p.current_terminal.tokenType,
                             TokenType.EOT)

    def test_parse_single_declaration_function_with_multiple_arguments(self):
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

            p.parse_single_declaration()

            self.assertEqual(p.current_terminal.tokenType,
                             TokenType.EOT)

    def test_parse_declaration_multiple(self):
        input_text = """
        int five ~ 5;
        str dog ~ wuf;
        (end)
        """
        with patch('builtins.open', mock_open(read_data=input_text)):
            s = Scanner('file')
            p = Parser(s)

            assert(p.current_terminal.spelling == 'int')
            p.parse_declaration()

            self.assertEqual(p.current_terminal.tokenType,
                             TokenType.LEFT_PAR)

    def test_parse_type_denoter(self):
        with patch('builtins.open', mock_open(read_data="int")):
            s = Scanner('file')
            p = Parser(s)

            assert(p.current_terminal.spelling == 'int')
            p.parse_declaration()

            self.assertEqual(p.current_terminal.tokenType,
                             TokenType.EOT)

    def test_parse_single_command_with_identifier_with_one_argument(self):
        with patch('builtins.open', mock_open(read_data='helloworld(123) ;')):
            s = Scanner('file')
            p = Parser(s)

            assert(p.current_terminal.tokenType is TokenType.IDENTIFIER)
            p.parse_single_command()

            self.assertEqual(
                p.current_terminal.tokenType, TokenType.SEMICOLON)

    def test_parse_single_command_with_identifier_with_multiple_arguments(self):
        with patch('builtins.open', mock_open(read_data='helloworld(123, hello, world) ;')):
            s = Scanner('file')
            p = Parser(s)

            assert(p.current_terminal.tokenType is TokenType.IDENTIFIER)
            p.parse_single_command()

            self.assertEqual(
                p.current_terminal.tokenType, TokenType.SEMICOLON)

    def test_parse_single_command_with_identifier_with_zero_arguments(self):
        with patch('builtins.open', mock_open(read_data='helloworld() ;')):
            s = Scanner('file')
            p = Parser(s)

            assert(p.current_terminal.tokenType is TokenType.IDENTIFIER)
            p.parse_single_command()

            self.assertEqual(
                p.current_terminal.tokenType, TokenType.SEMICOLON)

    def test_parse_expression_recursion_multiple_function_calls(self):
        with patch('builtins.open', mock_open(read_data='helloworld(arg) helloworld2() helloworld3(arg1, arg2) ;')):
            s = Scanner('file')
            p = Parser(s)

            assert(p.current_terminal.tokenType is TokenType.IDENTIFIER)
            p.parse_command()

            self.assertEqual(p.current_terminal.tokenType,
                             TokenType.SEMICOLON)
