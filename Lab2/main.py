from __future__ import annotations

import sys

from Lab2.src.Analyzer import Analyzer
from Lab2.src.ReportBuilder import ReportBuilder


class Main:
    def run(self) -> int:
        expression = self._read_expression()
        if not expression:
            print("Пустая формула не поддерживается.")
            return 1

        try:
            result = Analyzer().analyze(expression)
        except ValueError as error:
            print(f"Ошибка: {error}")
            return 1

        print(ReportBuilder().build(result))
        return 0

    def _read_expression(self) -> str:
        if len(sys.argv) > 1:
            return " ".join(sys.argv[1:]).strip()
        return input("Введите логическую формулу: ").strip()


if __name__ == "__main__":
    raise SystemExit(Main().run())