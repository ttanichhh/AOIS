import io
import unittest
from contextlib import redirect_stdout
from Lab1.arithmetic.FloatArithmetic import FloatArithmetic

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
