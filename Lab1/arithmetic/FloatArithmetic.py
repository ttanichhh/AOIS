from Lab1.converters.FloatConverter import FloatConverter


class FloatArithmetic:
    """Арифметика IEEE-754 (32 бита) поверх FloatConverter.
    FloatConverter отвечает за decimal <-> IEEE bits.
    IEEEArithmetic отвечает только за + - * / над битами.
    """

    def __init__(self):
        self.converter = FloatConverter()
        self.bit_size = self.converter.BIT_SIZE
        self.bias = 127
        self.mant_bits = 23
        self.expon_bits_and_1 = 9
        self.expon_bits = 8


    #  ВСПОМОГАТЕЛЬНОЕ

    def print_ieee_parts(self, bits, title=""):
        if title:
            print(title)
        print("sign:", bits[0])
        print("exponent:", "".join(map(str, bits[1:self.expon_bits_and_1])))
        print("mantissa:", "".join(map(str, bits[self.expon_bits_and_1:])))

    def _bits_to_int(self, bits):
        x = 0
        for b in bits:
            x = x * 2 + b
        return x

    def _int_to_bits(self, x, width):
        bits = [0] * width
        i = width - 1
        while i >= 0:
            bits[i] = x % 2
            x //= 2
            i -= 1
        return bits

    def unpack(self, bits):
        sign = bits[0]
        exp = self._bits_to_int(bits[1:self.expon_bits_and_1])
        mant_field = bits[self.expon_bits_and_1:]
        mant = self._bits_to_int(mant_field)

        if exp == 0 and mant == 0:
            return sign, 0, 0, True

        mant_24 = (1 << self.mant_bits) + mant  # 1.xxx
        return sign, exp, mant_24, False

    def pack(self, sign, exp, mant_24):
        bits = [0] * self.bit_size
        bits[0] = 1 if sign else 0

        if exp <= 0 or mant_24 == 0:
            return bits

        if exp >= 255:
            bits[1:self.expon_bits_and_1] = [1] * self.expon_bits
            return bits

        bits[1:self.expon_bits_and_1] = self._int_to_bits(exp, self.expon_bits)

        mant_field = mant_24 - (1 << self.mant_bits)
        bits[self.expon_bits_and_1:] = self._int_to_bits(mant_field, self.mant_bits)
        return bits

    def normalize(self, exp, mant_24):
        if mant_24 == 0:
            return 0, 0

        # если мантисса >= 2.0
        if mant_24 >= (1 << (self.mant_bits + 1)):  # >= 2^24
            mant_24 >>= 1
            exp += 1

        # если мантисса < 1.0
        while exp > 0 and mant_24 < (1 << self.mant_bits):
            mant_24 <<= 1
            exp -= 1

        return exp, mant_24

    #  ОПЕРАЦИИ НАД БИТАМИ

    def add_bits(self, a_bits, b_bits):
        a_sign, a_exp, a_mant, a_zero = self.unpack(a_bits)
        b_sign, b_exp, b_mant, b_zero = self.unpack(b_bits)

        if a_zero:
            return b_bits[:]
        if b_zero:
            return a_bits[:]

        exp = a_exp if a_exp >= b_exp else b_exp
        da = exp - a_exp
        db = exp - b_exp

        if da > 0:
            a_mant >>= da
        if db > 0:
            b_mant >>= db

        if a_sign == b_sign:
            mant = a_mant + b_mant
            sign = a_sign
        else:
            if a_mant >= b_mant:
                mant = a_mant - b_mant
                sign = a_sign
            else:
                mant = b_mant - a_mant
                sign = b_sign

        exp, mant = self.normalize(exp, mant)
        return self.pack(sign, exp, mant)

    def sub_bits(self, a_bits, b_bits):
        b2 = b_bits[:]
        b2[0] = 0 if b2[0] == 1 else 1
        return self.add_bits(a_bits, b2)

    def mul_bits(self, a_bits, b_bits):
        a_sign, a_exp, a_mant, a_zero = self.unpack(a_bits)
        b_sign, b_exp, b_mant, b_zero = self.unpack(b_bits)

        if a_zero or b_zero:
            return [0] * self.bit_size

        sign = a_sign ^ b_sign
        exp = a_exp + b_exp - self.bias

        product = a_mant * b_mant            # 48 бит
        mant = product >> self.mant_bits     # простое приведение

        exp, mant = self.normalize(exp, mant)
        return self.pack(sign, exp, mant)

    def div_bits(self, a_bits, b_bits):
        a_sign, a_exp, a_mant, a_zero = self.unpack(a_bits)
        b_sign, b_exp, b_mant, b_zero = self.unpack(b_bits)

        if b_zero:
            bits = [0] * self.bit_size
            bits[0] = a_sign ^ b_sign
            bits[1:self.expon_bits_and_1] = [1] * self.expon_bits
            return bits

        if a_zero:
            return [0] * self.bit_size

        sign = a_sign ^ b_sign
        exp = a_exp - b_exp + self.bias

        mant = (a_mant << self.mant_bits) // b_mant

        exp, mant = self.normalize(exp, mant)
        return self.pack(sign, exp, mant)

    #  ВЫВОД ДЛЯ ЛАБЫ

    def _show_operand(self, value, bits, title):
        print(title)
        print(f"Decimal: {value}")
        self.converter.print_bits(bits, "IEEE-754:")
        self.print_ieee_parts(bits)
        print()

    def _show_result(self, bits):
        self.converter.print_bits(bits, "IEEE-754 результат:")
        self.print_ieee_parts(bits, "Результат по полям:")
        print("В 10-ом формате (из битов):", self.converter.ieee754_to_decimal(bits))

    # ОПЕРАЦИИ С ВВОДОМ В DECIMAL

    def add(self, x, y):
        print("\nСЛОЖЕНИЕ IEEE-754")
        self.converter.convert(x)
        xb = self.converter.ieee_bits.copy()

        self.converter.convert(y)
        yb = self.converter.ieee_bits.copy()

        self._show_operand(x, xb, "Первое число:")
        self._show_operand(y, yb, "Второе число:")

        rb = self.add_bits(xb, yb)

        print("РЕЗУЛЬТАТ:")
        self._show_result(rb)
        return rb, self.converter.ieee754_to_decimal(rb)

    def sub(self, x, y):
        print("\nВЫЧИТАНИЕ IEEE-754")
        self.converter.convert(x)
        xb = self.converter.ieee_bits.copy()

        self.converter.convert(y)
        yb = self.converter.ieee_bits.copy()

        self._show_operand(x, xb, "Уменьшаемое:")
        self._show_operand(y, yb, "Вычитаемое:")

        rb = self.sub_bits(xb, yb)

        print("РЕЗУЛЬТАТ:")
        self._show_result(rb)
        return rb, self.converter.ieee754_to_decimal(rb)

    def mul(self, x, y):
        print("\nУМНОЖЕНИЕ IEEE-754")
        self.converter.convert(x)
        xb = self.converter.ieee_bits.copy()

        self.converter.convert(y)
        yb = self.converter.ieee_bits.copy()

        self._show_operand(x, xb, "Первый множитель:")
        self._show_operand(y, yb, "Второй множитель:")

        rb = self.mul_bits(xb, yb)

        print("РЕЗУЛЬТАТ:")
        self._show_result(rb)
        return rb, self.converter.ieee754_to_decimal(rb)

    def div(self, x, y):
        print("\nДЕЛЕНИЕ IEEE-754")
        self.converter.convert(x)
        xb = self.converter.ieee_bits.copy()

        self.converter.convert(y)
        yb = self.converter.ieee_bits.copy()

        self._show_operand(x, xb, "Делимое:")
        self._show_operand(y, yb, "Делитель:")

        rb = self.div_bits(xb, yb)

        print("РЕЗУЛЬТАТ:")
        self._show_result(rb)
        return rb, self.converter.ieee754_to_decimal(rb)