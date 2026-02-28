import io
import unittest
from contextlib import redirect_stdout

from Lab1.converters.IntConverter import IntConverter
from Lab1.converters.FloatConverter import FloatConverter

from Lab1.arithmetic.Composition import Composition
from Lab1.arithmetic.MultiplierDivider import MultiplierDivider
from Lab1.arithmetic.FloatArithmetic import FloatArithmetic
from Lab1.arithmetic.BCD8421Arithmetic import BCD8421Arithmetic


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


class TestFloatConverter(unittest.TestCase):
    def setUp(self):
        self.f = FloatConverter()

    def test_float_roundtrip_simple(self):
        for x in [0.0, 0.5, 0.75, 1.25, 2.5, -3.75, 10.0, -0.125]:
            bits = self.f.decimal_to_ieee754(x)
            back = self.f.ieee754_to_decimal(bits)
            self.assertAlmostEqual(back, x, places=6)

    def test_float_zero(self):
        bits = self.f.decimal_to_ieee754(0.0)
        self.assertEqual(sum(bits), 0)
        back = self.f.ieee754_to_decimal(bits)
        self.assertEqual(back, 0.0)


class TestFloatArithmetic(unittest.TestCase):
    def setUp(self):
        self.ar = FloatArithmetic()

    def test_add(self):
        with redirect_stdout(io.StringIO()):
            rb, dec = self.ar.add(1.5, 0.75)
        self.assertAlmostEqual(dec, 2.25, places=6)

    def test_sub(self):
        with redirect_stdout(io.StringIO()):
            rb, dec = self.ar.sub(2.5, 4.0)
        self.assertAlmostEqual(dec, -1.5, places=6)

    def test_mul(self):
        with redirect_stdout(io.StringIO()):
            rb, dec = self.ar.mul(-3.0, 1.25)
        self.assertAlmostEqual(dec, -3.75, places=6)



if __name__ == "__main__":
    unittest.main()