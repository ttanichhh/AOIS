import unittest
from Lab1.converters.IntConverter import IntConverter

class TestIntConverter(unittest.TestCase):
    def setUp(self):
        self.c = IntConverter()

    def test_decimal_to_direct_and_back_positive(self):
        for n in [0, 1, 2, 5, 13, 127, 1024, 123456]:
            bits = self.c.decimal_to_direct(n)
            self.assertEqual(bits[0], 0)
            back = self.c.direct_to_decimal(bits)
            self.assertEqual(back, n)

    def test_decimal_to_direct_and_back_negative(self):
        for n in [-1, -2, -5, -13, -127, -1024, -123456]:
            bits = self.c.decimal_to_direct(n)
            self.assertEqual(bits[0], 1)
            back = self.c.direct_to_decimal(bits)
            self.assertEqual(back, n)

    def test_inverse_and_twos_complement_roundtrip(self):
        for n in [-123, -1, 0, 1, 77, 999]:
            self.c.convert(n)
            twos = self.c.twos_complement_code[:]
            direct = self.c.twos_complement_to_direct(twos)
            back = self.c.direct_to_decimal(direct)
            self.assertEqual(back, n)

    def test_twos_complement_to_direct_negative_case(self):
        bits = [1] * self.c.BIT_SIZE  # -1 в two's complement
        direct = self.c.twos_complement_to_direct(bits)
        self.assertEqual(direct[0], 1)
        self.assertEqual(self.c.direct_to_decimal(direct), -1)
