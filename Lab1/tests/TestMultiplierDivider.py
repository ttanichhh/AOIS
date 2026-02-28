import io
import unittest
from contextlib import redirect_stdout
from Lab1.arithmetic.MultiplierDivider import MultiplierDivider


class TestMultiplierDivider(unittest.TestCase):
    def setUp(self):
        self.calc = MultiplierDivider()

    def test_multiply_sign_and_value(self):
        with redirect_stdout(io.StringIO()):
            bits, dec = self.calc.multiply(-3, 4)
        self.assertEqual(dec, -12)
        self.assertEqual(bits[0], 1)

        with redirect_stdout(io.StringIO()):
            bits2, dec2 = self.calc.multiply(3, 4)
        self.assertEqual(dec2, 12)
        self.assertEqual(bits2[0], 0)

    def test_multiply_by_zero(self):
        with redirect_stdout(io.StringIO()):
            bits, dec = self.calc.multiply(0, 123)
        self.assertEqual(dec, 0)

    def test_divide_basic_fixed_point(self):
        with redirect_stdout(io.StringIO()):
            bits, approx = self.calc.divide(5, 2)
        self.assertIsNotNone(bits)
        self.assertAlmostEqual(approx, 2.5, places=5)

    def test_divide_negative(self):
        with redirect_stdout(io.StringIO()):
            bits, approx = self.calc.divide(-5, 2)
        self.assertIsNotNone(bits)
        self.assertAlmostEqual(approx, -2.5, places=5)

    def test_divide_by_zero(self):
        with redirect_stdout(io.StringIO()):
            bits, approx = self.calc.divide(5, 0)
        self.assertIsNone(bits)
        self.assertIsNone(approx)
