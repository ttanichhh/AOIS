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
