from __future__ import annotations

from dataclasses import dataclass

from Lab2.src.TruthTable import TruthTableResult
from Lab2.src.ZhegalkinPolynomial import ZhegalkinPolynomial


@dataclass(frozen=True)
class PostClassesResult:
    t0: bool
    t1: bool
    s: bool
    m: bool
    l: bool


class PostClasses:
    def determine(self, table: TruthTableResult) -> PostClassesResult:
        if not table.rows:
            raise ValueError("Таблица истинности пуста.")

        return PostClassesResult(
            t0=table.rows[0].result == 0,
            t1=table.rows[-1].result == 1,
            s=self._is_self_dual(table),
            m=self._is_monotone(table),
            l=self._is_linear(table),
        )

    def _is_self_dual(self, table: TruthTableResult) -> bool:
        max_index = (1 << table.dimension) - 1
        for row in table.rows:
            opposite_result = table.rows[max_index ^ row.index].result
            if row.result == opposite_result:
                return False
        return True

    def _is_monotone(self, table: TruthTableResult) -> bool:
        for left_row in table.rows:
            for right_row in table.rows:
                dominates = all(
                    left_value <= right_value
                    for left_value, right_value in zip(
                        left_row.assignment,
                        right_row.assignment,
                    )
                )
                if dominates and left_row.result > right_row.result:
                    return False
        return True

    def _is_linear(self, table: TruthTableResult) -> bool:
        coefficients = ZhegalkinPolynomial().coefficients(table)
        for mask, coefficient in enumerate(coefficients):
            if coefficient == 1 and bin(mask).count("1") > 1:
                return False
        return True