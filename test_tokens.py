import unittest
from tokens import Token, TokenType


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
