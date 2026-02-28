class BCD8421Arithmetic:
    """Сложение чисел в 8421 BCD"""

    # Таблица 8421 BCD
    bcd_table = {
        0: [0,0,0,0],
        1: [0,0,0,1],
        2: [0,0,1,0],
        3: [0,0,1,1],
        4: [0,1,0,0],
        5: [0,1,0,1],
        6: [0,1,1,0],
        7: [0,1,1,1],
        8: [1,0,0,0],
        9: [1,0,0,1]
    }

    def decimal_to_bcd(self, num):
        #Перевод decimal → BCD
        digits = [int(d) for d in str(num)]
        bcd = []
        for d in digits:
            bcd.extend(self.bcd_table[d])
        return bcd

    def print_bcd(self, bcd, description=""):
        if description:
            print(description, end=" ")
        for i in range(0, len(bcd), 4):
            print("".join(map(str, bcd[i:i+4])), end=" ")
        print()

    def bcd_add_digit(self, a, b, carry):
        #Сложение одной BCD цифры
        result = [0]*4
        c = carry

        for i in range(3, -1, -1):
            s = a[i] + b[i] + c
            result[i] = s % 2
            c = s // 2

        # если > 9 → добавить 6
        if c == 1 or result > [1,0,0,1]:
            add6 = [0,1,1,0]
            c = 0
            for i in range(3, -1, -1):
                s = result[i] + add6[i] + c
                result[i] = s % 2
                c = s // 2
            return result, 1
        return result, 0

    def bcd_to_decimal(self, bcd):
        result = 0

        for i in range(0, len(bcd), 4):
            digit_bits = bcd[i:i + 4]

            # перевод 4 бит в число
            digit = 0
            for bit in digit_bits:
                digit = digit * 2 + bit

            result = result * 10 + digit

        return result

    def add(self, num1, num2):
        print("\nСЛОЖЕНИЕ В 8421 BCD")

        bcd1 = self.decimal_to_bcd(num1)
        bcd2 = self.decimal_to_bcd(num2)

        self.print_bcd(bcd1, f"{num1} в BCD:")
        self.print_bcd(bcd2, f"{num2} в BCD:")

        # выравнивание
        max_len = max(len(bcd1), len(bcd2))
        while len(bcd1) < max_len:
            bcd1 = [0,0,0,0] + bcd1
        while len(bcd2) < max_len:
            bcd2 = [0,0,0,0] + bcd2

        result = []
        carry = 0

        # складываем по цифрам
        for i in range(max_len-4, -1, -4):
            digit1 = bcd1[i:i+4]
            digit2 = bcd2[i:i+4]
            sum_digit, carry = self.bcd_add_digit(digit1, digit2, carry)
            result = sum_digit + result

        if carry:
            result = [0,0,0,1] + result

        print("\nРезультат в BCD:")
        self.print_bcd(result)

        decimal_result = self.bcd_to_decimal(result)
        print("В 10-ом формате:", decimal_result)

        return result