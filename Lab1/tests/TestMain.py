import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

# если твой main лежит в Lab1/main.py:
from Lab1.main import main


class TestMain(unittest.TestCase):

    def _run_main_with_inputs(self, inputs):
        """Запускает main() с подменённым input и без вывода в консоль."""
        with patch("builtins.input", side_effect=inputs):
            with redirect_stdout(io.StringIO()):
                main()

    def test_exit_from_main_menu(self):
        # сразу "6" -> выход
        self._run_main_with_inputs(["6"])

    def test_menu_1_int_converter(self):
        # 1 -> конвертер, число 5, потом выход 6
        self._run_main_with_inputs(["1", "5", "6"])

    def test_menu_2_composition_add_then_back_then_exit(self):
        # 2 -> доп.код
        # 1 -> сложение (composition сам спросит два числа)
        # 5 и 7
        # 3 -> назад
        # 6 -> выход
        self._run_main_with_inputs(["2", "1", "5", "7", "3", "6"])

    def test_menu_2_composition_sub_then_back_then_exit(self):
        # 2 -> доп.код
        # 2 -> вычитание (composition сам спросит два числа)
        # 10 и 3
        # 3 -> назад
        # 6 -> выход
        self._run_main_with_inputs(["2", "2", "10", "3", "3", "6"])

    def test_menu_3_multiply_then_back_then_exit(self):
        # 3 -> прямой код
        # 1 -> умножение
        # 3 и 4
        # 3 -> назад
        # 6 -> выход
        self._run_main_with_inputs(["3", "1", "3", "4", "3", "6"])

    def test_menu_3_divide_then_back_then_exit(self):
        # 3 -> прямой код
        # 2 -> деление
        # 5 и 2
        # 3 -> назад
        # 6 -> выход
        self._run_main_with_inputs(["3", "2", "5", "2", "3", "6"])

    def test_menu_4_ieee_add_then_back_then_exit(self):
        # 4 -> IEEE
        # 1 -> сложение
        # 1.5 и 0.75
        # 5 -> назад
        # 6 -> выход
        self._run_main_with_inputs(["4", "1", "1.5", "0.75", "5", "6"])

    def test_menu_4_ieee_sub_then_back_then_exit(self):
        # 4 -> IEEE
        # 2 -> вычитание
        # 2.5 и 4.0
        # 5 -> назад
        # 6 -> выход
        self._run_main_with_inputs(["4", "2", "2.5", "4.0", "5", "6"])

    def test_menu_4_ieee_mul_then_back_then_exit(self):
        # 4 -> IEEE
        # 3 -> умножение
        # -3.0 и 1.25
        # 5 -> назад
        # 6 -> выход
        self._run_main_with_inputs(["4", "3", "-3.0", "1.25", "5", "6"])

    def test_menu_4_ieee_div_then_back_then_exit(self):
        # 4 -> IEEE
        # 4 -> деление
        # 6.0 и 1.5
        # 5 -> назад
        # 6 -> выход
        self._run_main_with_inputs(["4", "4", "6.0", "1.5", "5", "6"])

    def test_menu_5_bcd_add_then_back_then_exit(self):
        # 5 -> BCD
        # 1 -> сложение
        # 12 и 34
        # 2 -> назад
        # 6 -> выход
        self._run_main_with_inputs(["5", "1", "12", "34", "2", "6"])

    def test_invalid_choices(self):
        # неверный выбор в главном меню, потом выход
        self._run_main_with_inputs(["999", "6"])