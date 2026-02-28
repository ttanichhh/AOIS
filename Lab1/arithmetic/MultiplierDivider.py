from Lab1.arithmetic.Composition import Composition
from Lab1.converters.IntConverter import IntConverter


class MultiplierDivider:
    """Умножения и деления в прямом двоичном коде."""

    frac_bits = 5  # 5 двоичных знаков после точки

    def __init__(self):
        self.converter = IntConverter()
        self.composition = Composition()
        self.bit_size = self.converter.BIT_SIZE

    # ПЕЧАТЬ / КОНВЕРТИРУЕМ
    # Печатает число в прямом коде и возвращает массив бит
    def print_number_direct_code(self, num, header=""):
        self.converter.convert(num)
        bits = self.converter.direct_code.copy()
        if header:
            print(header)
        self.converter.print_bits(bits)
        return bits

    # Печатает прямые коды введённых чисел и возвращает (bits1, bits2)
    def print_input_direct_codes(self, num1, num2):
        bits1 = self.print_number_direct_code(num1, f"\n{num1} в прямом коде:")
        bits2 = self.print_number_direct_code(num2, f"{num2} в прямом коде:")
        return bits1, bits2

    #Строка +/-<целая часть>.<5бит дроби>
    def format_fixed_point_binary(self, bits):
        sign = '-' if bits[0] == 1 else '+'
        mag = bits[1:]  # 31 бит
        cut = len(mag) - self.frac_bits
        int_part = mag[:cut]
        frac_part = mag[cut:]
        return f"{sign}{''.join(map(str, int_part))}.{''.join(map(str, frac_part))}"

    # Перевод 5 двоичных дробных бит в 10-ое для проверки (ручной).
    def fixed_to_decimal(self, bits):
        sign = -1 if bits[0] == 1 else 1

        # целая часть
        int_value = 0
        for i in range(1, self.bit_size - self.frac_bits):
            int_value = int_value * 2 + bits[i]

        # дробная часть
        frac_value = 0.0
        weight = 0.5
        for i in range(self.bit_size - self.frac_bits, self.bit_size):
            if bits[i] == 1:
                frac_value += weight
            weight /= 2

        return sign * (int_value + frac_value)

    # модуль

    def get_abs_bits(self, bits):
        out = bits[:]
        out[0] = 0
        return out

    def is_zero_mag(self, bits):
        for i in range(1, self.bit_size):
            if bits[i] == 1:
                return False
        return True

    # cравнение модулей без знака: возвращает -1 / 0 / 1.
    def compare_mag(self, a, b):
        for i in range(1, self.bit_size):
            if a[i] != b[i]:
                return 1 if a[i] > b[i] else -1
        return 0

    # Сдвиг влево только модуля (bit0 = 0).
    def shift_left_mag(self, bits, count=1):
        out = bits[:]
        out[0] = 0
        for _ in range(count):
            for i in range(1, self.bit_size - 1):
                out[i] = out[i + 1]
            out[self.bit_size - 1] = 0
        return out

    # a - b по модулю, предполагается a >= b.
    def sub_mag(self, a, b):
        out = a[:]
        out[0] = 0
        borrow = 0
        for i in range(self.bit_size - 1, 0, -1):
            val = out[i] - b[i] - borrow
            if val >= 0:
                out[i] = val
                borrow = 0
            else:
                out[i] = val + 2
                borrow = 1
        return out

    # деление для модуля без знака. Возвращает (частное, остаток)
    def div_restoring_mag(self, dividend, divisor):
        if self.is_zero_mag(divisor):
            raise ZeroDivisionError("деление на ноль")

        # модули делимого и делителя
        q = dividend[:]
        q[0] = 0

        d = divisor[:]
        d[0] = 0

        r = [0] * self.bit_size #остаток

        #сдвигается влево
        for _ in range(self.bit_size - 1):
            # (r, q) <<= 1
            msb_q = q[1]
            r = self.shift_left_mag(r, 1)
            r[self.bit_size - 1] = msb_q
            q = self.shift_left_mag(q, 1)

            # если r >= d: r -= d; q_lsb = 1
            if self.compare_mag(r, d) >= 0:
                r = self.sub_mag(r, d)
                q[self.bit_size - 1] = 1
            else:
                q[self.bit_size - 1] = 0

        return q, r

    # ------------------- УМНОЖЕНИЕ -------------------

    def multiply(self, num1, num2):
        print("\nУМНОЖЕНИЕ")

        # выводим введённые числа в прямом коде
        bits1, bits2 = self.print_input_direct_codes(num1, num2)

        sign = bits1[0] ^ bits2[0] # Это операция XOR (исключающее ИЛИ).

        multiplicand = self.get_abs_bits(bits1)
        multiplier = self.get_abs_bits(bits2)

        result = [0] * self.bit_size

        # "сдвиг + сложение"
        for i in range(self.bit_size - 1, 0, -1):
            if multiplier[i] == 1:
                shifted = self.shift_left_mag(multiplicand, self.bit_size - 1 - i)
                result = self.composition.add_binary(result, shifted)

        result[0] = sign

        print("\nРезультат в двоичном виде:")
        self.converter.print_bits(result)

        # перевод результата умножения в 10-ое (через уже готовую функцию)
        decimal_result = self.converter.direct_to_decimal(result)
        print("\nВ 10-ом формате (из битов):", decimal_result)

        return result, decimal_result

    # ------------------- ДЕЛЕНИЕ-------------------

    def divide(self, num1, num2):
        print("\nДЕЛЕНИЕ")

        if num2 == 0:
            print("Ошибка: деление на 0")
            return None, None

        # выводим введённые числа в прямом коде
        bits1, bits2 = self.print_input_direct_codes(num1, num2)

        sign = bits1[0] ^ bits2[0]

        a = self.get_abs_bits(bits1)  # |num1|
        b = self.get_abs_bits(bits2)  # |num2|

        if self.is_zero_mag(b):
            print("Ошибка: деление на 0")
            return None, None

        # сдвиг числа a влево на 5 бит умножение на 2^5=32:
        # (добавляет места для дробной части, делит как обычные числа и вернет знак)
        a_scaled = self.shift_left_mag(a, self.frac_bits) # делимое умножается на 32

        q_fixed, _ = self.div_restoring_mag(a_scaled, b)
        q_fixed[0] = sign

        print("Результат:", self.format_fixed_point_binary(q_fixed))

        # десятичное значение, восстановленное из битов
        approx = self.fixed_to_decimal(q_fixed)
        print("\nВ 10-ом формате (из битов):", approx)

        return q_fixed, approx