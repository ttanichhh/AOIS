from Lab1.converters.IntConverter import IntConverter
from Lab1.arithmetic.Composition import Composition
from Lab1.arithmetic.MultiplierDivider import MultiplierDivider
from Lab1.arithmetic.FloatArithmetic import FloatArithmetic
from Lab1.arithmetic.BCD8421Arithmetic import BCD8421Arithmetic


def main():

    int_converter = IntConverter()
    composition = Composition()
    direct = MultiplierDivider()
    ieee = FloatArithmetic()
    bcd = BCD8421Arithmetic()

    while True:
        print("\n" + "=" * 60)
        print("ЛАБОРАТОРНАЯ РАБОТА 1")
        print("1. Перевод числа (прямой / обратный / дополнительный)")
        print("2. Сложение / Вычитание (дополнительный код)")
        print("3. Умножение / Деление (прямой код)")
        print("4. IEEE-754 операции")
        print("5. 8421 BCD сложение")
        print("6. Выход")
        print("=" * 60)

        choice = input("Ваш выбор: ").strip()

        # INT CONVERTER
        if choice == "1":
            number = int(input("Введите число: "))
            int_converter.convert(number)
            int_converter.display_results()

        # ДОПОЛНИТЕЛЬНЫЙ КОД
        elif choice == "2":
            while True:
                print("\nСЛОЖЕНИЕ / ВЫЧИТАНИЕ")
                print("1. Сложение")
                print("2. Вычитание")
                print("3. Назад")

                sub_choice = input("Ваш выбор: ")

                if sub_choice == "1":
                    composition.calculate('+')
                elif sub_choice == "2":
                    composition.calculate('-')
                elif sub_choice == "3":
                    break
                else:
                    print("Неверный выбор")

        # ПРЯМОЙ КОД
        elif choice == "3":
            while True:
                print("\nУМНОЖЕНИЕ / ДЕЛЕНИЕ")
                print("1. Умножение")
                print("2. Деление")
                print("3. Назад")

                sub_choice = input("Ваш выбор: ")

                if sub_choice == "1":
                    num1 = int(input("Введите первое число: "))
                    num2 = int(input("Введите второе число: "))
                    direct.multiply(num1, num2)

                elif sub_choice == "2":
                    num1 = int(input("Введите делимое: "))
                    num2 = int(input("Введите делитель: "))
                    direct.divide(num1, num2)

                elif sub_choice == "3":
                    break
                else:
                    print("Неверный выбор")

        # IEEE
        elif choice == "4":
            while True:
                print("\nIEEE-754 операции")
                print("1. Сложение")
                print("2. Вычитание")
                print("3. Умножение")
                print("4. Деление")
                print("5. Назад")

                sub_choice = input("Ваш выбор: ")

                if sub_choice == "1":
                    x = float(input("Введите x: "))
                    y = float(input("Введите y: "))
                    ieee.add(x, y)

                elif sub_choice == "2":
                    x = float(input("Введите x: "))
                    y = float(input("Введите y: "))
                    ieee.sub(x, y)

                elif sub_choice == "3":
                    x = float(input("Введите x: "))
                    y = float(input("Введите y: "))
                    ieee.mul(x, y)

                elif sub_choice == "4":
                    x = float(input("Введите x: "))
                    y = float(input("Введите y: "))
                    ieee.div(x, y)

                elif sub_choice == "5":
                    break
                else:
                    print("Неверный выбор")

        # BCD
        elif choice == "5":
            while True:
                print("\n8421 BCD")
                print("1. Сложение")
                print("2. Назад")

                sub_choice = input("Ваш выбор: ")

                if sub_choice == "1":
                    a = int(input("Введите первое число: "))
                    b = int(input("Введите второе число: "))
                    bcd.add(a, b)

                elif sub_choice == "2":
                    break
                else:
                    print("Неверный выбор")

        elif choice == "6":
            print("До свидания!")
            break

        else:
            print("Неверный выбор")

if __name__ == "__main__":
    main()