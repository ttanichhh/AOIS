from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from Lab2.src.TruthTable import TruthTableResult


@dataclass(frozen=True)
class ZhegalkinPolynomialResult:
    coefficients: Tuple[int, ...]
    monomials: Tuple[str, ...]
    expression: str


class ZhegalkinPolynomial:
    def build(self, table: TruthTableResult) -> ZhegalkinPolynomialResult:
        coefficients = self.coefficients(table)
        monomials = tuple(
            self._mask_to_monomial(mask, table.variables)
            for mask, coefficient in enumerate(coefficients)
            if coefficient == 1
        )
        expression = " ^ ".join(monomials) if monomials else "0"

        return ZhegalkinPolynomialResult(
            coefficients=coefficients,
            monomials=monomials,
            expression=expression,
        )

    def coefficients(self, table: TruthTableResult) -> Tuple[int, ...]:
        coefficients = list(table.vector)

        for bit in range(table.dimension):
            bit_mask = 1 << bit
            for mask in range(1 << table.dimension):
                if mask & bit_mask:
                    coefficients[mask] ^= coefficients[mask ^ bit_mask]

        return tuple(coefficients)

    def _mask_to_monomial(self, mask: int, variables: Tuple[str, ...]) -> str:
        if mask == 0:
            return "1"

        parts = []
        dimension = len(variables)
        for index, variable in enumerate(variables):
            bit = 1 << (dimension - 1 - index)
            if mask & bit:
                parts.append(variable)

        return "*".join(parts)