from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Dict, Iterable, Tuple

from Lab2.src.CanonicalForms import CanonicalForms
from Lab2.src.TruthTable import TruthTable, TruthTableResult


@dataclass(frozen=True)
class BooleanDerivativeResult:
    by_variables: Tuple[str, ...]
    order: int
    vector: Tuple[int, ...]
    sdnf: str
    numeric_form: Tuple[int, ...]
    index_vector: str
    index_number: int


class BooleanDerivative:
    def find_fictitious_variables(self, table: TruthTableResult) -> Tuple[str, ...]:
        if table.dimension == 0:
            return tuple()

        fictitious = []
        for index, variable in enumerate(table.variables):
            bit_mask = 1 << (table.dimension - 1 - index)
            if self._is_fictitious(table, bit_mask):
                fictitious.append(variable)

        return tuple(fictitious)

    def build_all(
        self,
        table: TruthTableResult,
        max_order: int = 4,
    ) -> Tuple[BooleanDerivativeResult, ...]:
        derivatives = []
        supported_order = min(max_order, table.dimension)

        for order in range(1, supported_order + 1):
            for variables_group in combinations(table.variables, order):
                derivatives.append(self.build(table, variables_group))

        return tuple(derivatives)

    def build(
        self,
        table: TruthTableResult,
        by_variables: Tuple[str, ...],
    ) -> BooleanDerivativeResult:
        if not by_variables:
            raise ValueError("Для вычисления производной нужна хотя бы одна переменная.")

        variable_to_mask: Dict[str, int] = {
            variable: 1 << (table.dimension - 1 - index)
            for index, variable in enumerate(table.variables)
        }

        unknown_variables = [
            name for name in by_variables if name not in variable_to_mask
        ]
        if unknown_variables:
            raise ValueError(f"Неизвестные переменные: {unknown_variables}")

        masks = self._build_masks(variable_to_mask[name] for name in by_variables)
        derivative_vector = []

        for index in range(1 << table.dimension):
            value = 0
            for mask in masks:
                value ^= table.vector[index ^ mask]
            derivative_vector.append(value)

        derivative_table = TruthTable().from_vector(
            table.variables,
            derivative_vector,
        )
        canonical = CanonicalForms().build(derivative_table)

        return BooleanDerivativeResult(
            by_variables=by_variables,
            order=len(by_variables),
            vector=tuple(derivative_vector),
            sdnf=canonical.sdnf,
            numeric_form=canonical.sdnf_numeric,
            index_vector=canonical.index_vector,
            index_number=canonical.index_number,
        )

    def _is_fictitious(self, table: TruthTableResult, bit_mask: int) -> bool:
        for index in range(1 << table.dimension):
            if index & bit_mask:
                continue
            if table.vector[index] != table.vector[index | bit_mask]:
                return False
        return True

    def _build_masks(self, bits: Iterable[int]) -> Tuple[int, ...]:
        masks = [0]
        for bit in bits:
            masks.extend(mask | bit for mask in list(masks))
        return tuple(masks)