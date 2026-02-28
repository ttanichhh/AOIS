class FloatConverter:
    BIT_SIZE = 32

    def __init__(self, number=None):
        self.number = number
        self.ieee_bits = None
        self.decimal_value = None

        if number is not None:
            self.convert(number)

    #  DECIMAL → IEEE

    def decimal_to_ieee754(self, n):
        bits = [0] * self.BIT_SIZE

        # знак
        if n < 0:
            bits[0] = 1
            n = -n
        else:
            bits[0] = 0

        if n == 0:
            return bits

        integer = int(n) # целая часть
        fraction = n - integer # дробная часть

        # целая часть
        int_bits = []
        if integer == 0:
            int_bits = [0]
        else:
            while integer > 0:
                int_bits.insert(0, integer % 2)
                integer //= 2

        # дробная часть
        frac_bits = []
        while fraction > 0 and len(frac_bits) < 30:
            fraction *= 2
            bit = int(fraction)
            frac_bits.append(bit)
            fraction -= bit

        # нормализация
        if int_bits != [0]:
            shift = len(int_bits) - 1
            mantissa_source = int_bits[1:] + frac_bits
        else:
            shift = -1
            i = 0
            while i < len(frac_bits) and frac_bits[i] == 0:
                shift -= 1
                i += 1
            mantissa_source = frac_bits[i+1:]

        exponent = shift + 127

        # экспонента
        exp_bits = [0]*8
        i = 7
        while exponent > 0 and i >= 0:
            exp_bits[i] = exponent % 2
            exponent //= 2
            i -= 1

        bits[1:9] = exp_bits

        # мантисса
        mantissa = mantissa_source[:23]
        while len(mantissa) < 23:
            mantissa.append(0)

        bits[9:] = mantissa

        return bits

    # IEEE → DECIMAL

    def ieee754_to_decimal(self, bits):
        sign = -1 if bits[0] == 1 else 1

        # экспонента (raw)
        exponent_raw = 0
        for i in range(1, 9):
            exponent_raw = exponent_raw * 2 + bits[i]

        # проверяем мантиссу на нули
        mantissa_all_zero = True
        for i in range(9, 32):
            if bits[i] == 1:
                mantissa_all_zero = False
                break

        # exp=0 и mantissa=0 => 0.0
        if exponent_raw == 0 and mantissa_all_zero:
            return 0.0

        exponent = exponent_raw - 127

        # мантисса (начинается с 1.)
        mantissa = 1
        weight = 0.5
        for i in range(9, 32):
            if bits[i] == 1:
                mantissa += weight
            weight /= 2

        return sign * mantissa * (2 ** exponent)
    # ОСНОВНОЙ МЕТОД

    def convert(self, number):
        self.number = number
        self.ieee_bits = self.decimal_to_ieee754(number)
        self.decimal_value = self.ieee754_to_decimal(self.ieee_bits)
        return self

    def print_bits(self, bits, description=""):
        if description:
            print(description, end=" ")
        for bit in bits:
            print(bit, end='')
        print()

    def display_results(self):
        if self.number is None:
            print("Введите число!")
            return

        print(f"\nЧисло: {self.number}")
        print("IEEE-754 (32 бита):")
        self.print_bits(self.ieee_bits)

        print("sign:", self.ieee_bits[0])
        print("exponent:", "".join(map(str, self.ieee_bits[1:9])))
        print("mantissa:", "".join(map(str, self.ieee_bits[9:])))

        print("\nОбратное преобразование:")
        print("Decimal:", self.decimal_value)