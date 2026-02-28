import unittest
from Lab1.converters.IntConverter import IntConverter
from Lab1.arithmetic.Composition import Composition

class TestComposition(unittest.TestCase):
    def setUp(self):
        self.comp = Composition()
        self.c = IntConverter()

    def test_add_binary_basic(self):
        self.c.convert(5)
        a = self.c.twos_complement_code[:]
        self.c.convert(7)
        b = self.c.twos_complement_code[:]

        res = self.comp.add_binary(a, b)
        direct = self.c.twos_complement_to_direct(res)
        self.assertEqual(self.c.direct_to_decimal(direct), 12)

    def test_add_binary_negative(self):
        self.c.convert(-5)
        a = self.c.twos_complement_code[:]
        self.c.convert(2)
        b = self.c.twos_complement_code[:]

        res = self.comp.add_binary(a, b)
        direct = self.c.twos_complement_to_direct(res)
        self.assertEqual(self.c.direct_to_decimal(direct), -3)
