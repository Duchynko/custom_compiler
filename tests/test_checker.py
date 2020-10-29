import unittest

from abstract_tree.terminals import Identifier
from checker import Checker


class TestChecker(unittest.TestCase):
    def test_visit_identifier(self):
        ch = Checker()

        identifier = ch.visit_identifier(Identifier("Hello"))
        self.assertEqual(identifier, "Hello")
