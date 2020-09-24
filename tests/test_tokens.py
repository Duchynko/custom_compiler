import unittest
from tokens import Token, TokenType, ASSIGNOPS


class TestTokens(unittest.TestCase):
    def test_init(self):
        token = Token(TokenType.IDENTIFIER, '')

        self.assertEqual(token.tokenType, TokenType.IDENTIFIER)
        self.assertNotEqual(token, None)

    def test_init_with_keyword(self):
        token = Token(TokenType.IDENTIFIER, 'func')

        self.assertEqual(token.spelling, 'func')
        self.assertEqual(token.tokenType, TokenType.FUNC)

    def test_init_two(self):
        keyword = Token(TokenType.IDENTIFIER, 'return')
        operator = Token(TokenType.OPERATOR, '+')

        self.assertEqual(keyword.tokenType, TokenType.RETURN)
        self.assertEqual(operator.tokenType, TokenType.OPERATOR)

    def test_contains_operator_true(self):
        operator = Token(TokenType.OPERATOR, '~')

        result = operator.is_type_of_operator(ASSIGNOPS)

        self.assertTrue(result)

    def test_contains_operator_false(self):
        operator = Token(TokenType.OPERATOR, '+')

        result = operator.is_type_of_operator(ASSIGNOPS)

        self.assertFalse(result)

    def test_contains_operator_invalid_token(self):
        operator = Token(TokenType.OPERATOR, 'A')

        result = operator.is_type_of_operator(ASSIGNOPS)

        self.assertFalse(result)

    def test_is_assign_operator_true(self):
        token = Token(TokenType.OPERATOR, '~')

        self.assertTrue(token.is_assign_operator())

    def test_is_assign_operator_false(self):
        token = Token(TokenType.OPERATOR, '+')

        self.assertFalse(token.is_assign_operator())

    def test_is_mul_operator_true(self):
        token = Token(TokenType.OPERATOR, '*')

        self.assertTrue(token.is_mul_operator())

    def test_is_mul_operator_false(self):
        token = Token(TokenType.OPERATOR, '+')

        self.assertFalse(token.is_mul_operator())

    def test_is_add_operator_true(self):
        token = Token(TokenType.OPERATOR, '+')

        self.assertTrue(token.is_add_operator())

    def test_is_add_operator_false(self):
        token = Token(TokenType.OPERATOR, '/')

        self.assertFalse(token.is_add_operator())
