class IntConverter:
    # Размер числа
    BIT_SIZE = 32

    def __init__(self, number=None):
        self.number = number
        self.direct_code = None
        self.inverse_code = None
        self.twos_complement_code = None

        # проверка ввели ли число
        if number is not None:
            self.convert(number)

    #конвертируем в двоичную
    def decimal_to_direct(self, n):
        bits = [0] * self.BIT_SIZE

        # Определяем знак
        if n < 0:
            bits[0] = 1
            n = -n
        else:
            bits[0] = 0

        # Заполняем число справа налево (31 бит)
        i = self.BIT_SIZE - 1
        while n > 0 and i > 0:
            bits[i] = n % 2
            n = n // 2
            i -= 1

        return bits

    # в обратный
    def direct_to_inverse(self, bits):
        result = bits[:]  # копия массива

        # Если число отрицательное — инвертируем биты числа
        if result[0] == 1:
            for i in range(1, self.BIT_SIZE):
                if result[i] == 0:
                    result[i] = 1
                else:
                    result[i] = 0

        return result

    def inverse_to_twos_complement(self, bits):
        result = bits[:]

        # Если число отрицательное — прибавляем 1
        if result[0] == 1:
            carry = 1
            for i in range(self.BIT_SIZE - 1, -1, -1):
                total = result[i] + carry
                result[i] = total % 2
                carry = total // 2

        return result

    # из дополнительного в прямой
    def twos_complement_to_direct(self, bits):
        result = bits[:]

        # Если число отрицательное (первый бит = 1)
        if result[0] == 1:
            # -1
            borrow = 1
            for i in range(self.BIT_SIZE - 1, -1, -1):
                if result[i] >= borrow:
                    result[i] = result[i] - borrow
                    borrow = 0
                else:
                    result[i] = result[i] + 2 - borrow
                    borrow = 1

            # Инвертируем все биты (кроме первого)
            for i in range(1, self.BIT_SIZE):
                result[i] = 1 - result[i]

        return result

    # из двоичного числа в десятичное
    def direct_to_decimal(self, bits):
        # Проверяем знак
        if bits[0] == 0:
            # Положительное число
            result = 0
            # тут накоплением конвертируется
            for i in range(1, self.BIT_SIZE):
                result = result * 2 + bits[i]
            return result
        else:
            # Отрицательное число
            result = 0
            for i in range(1, self.BIT_SIZE):
                result = result * 2 + bits[i]
            return -result

    def print_bits(self, bits, description=""):
        if description:
            print(description, end=" ")
        for bit in bits:
            print(bit, end='')
        print()

    def convert(self, number):
        #Выполняем все преобразования для заданного числа
        self.number = number
        self.direct_code = self.decimal_to_direct(number)
        self.inverse_code = self.direct_to_inverse(self.direct_code)
        self.twos_complement_code = self.inverse_to_twos_complement(self.inverse_code)
        return self

    def display_results(self):
        #на экран
        if self.number is None:
            print("Сначала введите число или вызовите convert()")
            return

        print(f"\nЧисло: {self.number}")
        print("\nПрямой код:")
        self.print_bits(self.direct_code)

        print("\nОбратный код:")
        self.print_bits(self.inverse_code)

        print("\nДополнительный код:")
        self.print_bits(self.twos_complement_code)
