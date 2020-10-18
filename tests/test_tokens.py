import unittest
from tokens import Token, Kind, ASSIGNOPS


class TestTokens(unittest.TestCase):
    def test_init(self):
        token = Token(Kind.IDENTIFIER, '')

        self.assertEqual(token.kind, Kind.IDENTIFIER)
        self.assertNotEqual(token, None)

    def test_init_with_keyword(self):
        token = Token(Kind.IDENTIFIER, 'func')

        self.assertEqual(token.spelling, 'func')
        self.assertEqual(token.kind, Kind.FUNC)

    def test_init_two(self):
        keyword = Token(Kind.IDENTIFIER, 'return')
        operator = Token(Kind.OPERATOR, '+')

        self.assertEqual(keyword.kind, Kind.RETURN)
        self.assertEqual(operator.kind, Kind.OPERATOR)

    def test_contains_operator_true(self):
        operator = Token(Kind.OPERATOR, '~')

        result = operator.is_type_of_operator(ASSIGNOPS)

        self.assertTrue(result)

    def test_contains_operator_false(self):
        operator = Token(Kind.OPERATOR, '+')

        result = operator.is_type_of_operator(ASSIGNOPS)

        self.assertFalse(result)

    def test_contains_operator_invalid_token(self):
        operator = Token(Kind.OPERATOR, 'A')

        result = operator.is_type_of_operator(ASSIGNOPS)

        self.assertFalse(result)

    def test_is_assign_operator_true(self):
        token = Token(Kind.OPERATOR, '~')

        self.assertTrue(token.is_assign_operator())

    def test_is_assign_operator_false(self):
        token = Token(Kind.OPERATOR, '+')

        self.assertFalse(token.is_assign_operator())

    def test_is_mul_operator_true(self):
        token = Token(Kind.OPERATOR, '*')

        self.assertTrue(token.is_mul_operator())

    def test_is_mul_operator_false(self):
        token = Token(Kind.OPERATOR, '+')

        self.assertFalse(token.is_mul_operator())

    def test_is_add_operator_true(self):
        token = Token(Kind.OPERATOR, '+')

        self.assertTrue(token.is_add_operator())

    def test_is_add_operator_false(self):
        token = Token(Kind.OPERATOR, '/')

        self.assertFalse(token.is_add_operator())
