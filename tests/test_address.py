from unittest import TestCase

from address import Address


class TestAddress(TestCase):
    def test_from_address_without_increment_arg(self):
        a1 = Address(10, 11)
        a2 = Address().from_address(address=a1)

        self.assertEqual(a2.level, 11)
        self.assertEqual(a2.displacement, 0)

    def test_from_address_with_increment_arg(self):
        a1 = Address(10, 11)
        a2 = Address().from_address(address=a1, increment=1)

        self.assertEqual(a2.level, 10)
        self.assertEqual(a2.displacement, 12)

    def test_str(self):
        a1 = Address(10, 11)

        self.assertEqual(str(a1), f"Level={a1.level}, displacement={a1.displacement}")