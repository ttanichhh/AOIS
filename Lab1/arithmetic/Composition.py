from Lab1.converters.IntConverter import IntConverter


class Composition:
    """Класс для арифметических операций в дополнительном коде"""

    def __init__(self):
        self.converter = IntConverter()
        self.num1 = None
        self.num2 = None
        self.result_binary = None
        self.result_decimal = None

    # складываем числа в двоичном коде
    def add_binary(self, bits1, bits2):
        result = [0] * self.converter.BIT_SIZE
        carry = 0

        for i in range(self.converter.BIT_SIZE - 1, -1, -1):
            total = bits1[i] + bits2[i] + carry
            result[i] = total % 2
            carry = total // 2

        return result

    # ввод чисел проверка
    def get_number(self, prompt):
        while True:
            try:
                user_input = input(prompt).strip()
                if user_input == '':
                    print("Введите число!")
                    continue
                return int(user_input)
            except ValueError:
                print("Это должно быть целое число!")

    # подготовка данных для сложения
    def prepare_addition(self):
        print("\nСЛОЖЕНИЕ")
        self.num1 = self.get_number("Введите первое число: ")
        self.num2 = self.get_number("Введите второе число: ")

        # Получаем дополнительные коды через конвертер
        self.converter.convert(self.num1)
        tc1 = self.converter.twos_complement_code.copy()

        self.converter.convert(self.num2)
        tc2 = self.converter.twos_complement_code.copy()

        # Выводим числа через конвертер
        print(f"\n{self.num1} в дополнительном коде:")
        self.converter.print_bits(tc1)
        print(f"{self.num2} в дополнительном коде:")
        self.converter.print_bits(tc2)

        return tc1, tc2, self.num1 + self.num2, '+'

    # подготовка данных для вычитания
    def prepare_subtraction(self):
        print("\nВЫЧИТАНИЕ")
        self.num1 = self.get_number("Введите уменьшаемое: ")
        self.num2 = self.get_number("Введите вычитаемое: ")

        # Получаем дополнительный код уменьшаемого через конвертер
        self.converter.convert(self.num1)
        tc1 = self.converter.twos_complement_code.copy()

        # Получаем дополнительный код для -вычитаемого через конвертер
        self.converter.convert(-self.num2)
        tc2 = self.converter.twos_complement_code.copy()

        # Выводим числа через конвертер
        print(f"\n{self.num1} в дополнительном коде:")
        self.converter.print_bits(tc1)
        print(f"-{self.num2} в дополнительном коде:")
        self.converter.print_bits(tc2)

        return tc1, tc2, self.num1 - self.num2, '-'

    # вывод результата
    def display_result(self, expected, op_symbol):
        # Выводим результат в двоичном виде через конвертер
        print("\nРезультат в двоичном виде:")
        self.converter.print_bits(self.result_binary)

        # Переводим обратно в десятичное через конвертер
        direct_result = self.converter.twos_complement_to_direct(self.result_binary)
        self.result_decimal = self.converter.direct_to_decimal(direct_result)

        # Вывод результатов в десятичном виде
        print(f"\n{self.num1} {op_symbol} {self.num2} = {self.result_decimal}")
        print(f"Проверка: {expected}")

        if self.result_decimal == expected:
            print("Проверку прошло.")
        else:
            print("Ошибка!")

    # основная функция
    def calculate(self, operation):
        if operation == '+':
            tc1, tc2, expected, op_symbol = self.prepare_addition()
        elif operation == '-':
            tc1, tc2, expected, op_symbol = self.prepare_subtraction()
        else:
            print("Неизвестная операция")
            return

        # Складываем
        self.result_binary = self.add_binary(tc1, tc2)

        # Выводим результат
        self.display_result(expected, op_symbol)
