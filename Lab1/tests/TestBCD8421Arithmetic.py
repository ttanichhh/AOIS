import io
import unittest
from contextlib import redirect_stdout
from Lab1.arithmetic.BCD8421Arithmetic import BCD8421Arithmetic

class TestBCD8421Arithmetic(unittest.TestCase):
    def setUp(self):
        self.bcd = BCD8421Arithmetic()

    def test_decimal_to_bcd_and_back(self):
        for n in [0, 7, 12, 85, 125, 999, 1024]:
            b = self.bcd.decimal_to_bcd(n)
            back = self.bcd.bcd_to_decimal(b)
            self.assertEqual(back, n)

    def test_bcd_add_no_carry(self):
        with redirect_stdout(io.StringIO()):
            res = self.bcd.add(12, 34)
        self.assertEqual(self.bcd.bcd_to_decimal(res), 46)

    def test_bcd_add_with_inner_carry(self):
        with redirect_stdout(io.StringIO()):
            res = self.bcd.add(27, 58)
        self.assertEqual(self.bcd.bcd_to_decimal(res), 85)

    def test_bcd_add_with_new_digit(self):
        with redirect_stdout(io.StringIO()):
            res = self.bcd.add(58, 67)
        self.assertEqual(self.bcd.bcd_to_decimal(res), 125)
