from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Dict, Iterable, Tuple

from Lab2.src.ExpressionParser import ParsedExpression


@dataclass(frozen=True)
class TruthRow:
    assignment: Tuple[int, ...]
    result: int
    index: int


@dataclass(frozen=True)
class TruthTableResult:
    variables: Tuple[str, ...]
    rows: Tuple[TruthRow, ...]

    @property
    def vector(self) -> Tuple[int, ...]:
        return tuple(row.result for row in self.rows)

    @property
    def dimension(self) -> int:
        return len(self.variables)


class TruthTable:
    def build(self, parsed_expression: ParsedExpression) -> TruthTableResult:
        variables = parsed_expression.variables

        if not variables:
            result = parsed_expression.root.evaluate({})
            row = TruthRow(tuple(), result, 0)
            return TruthTableResult(variables, (row,))

        rows = []
        for values in product((0, 1), repeat=len(variables)):
            assignment: Dict[str, int] = dict(zip(variables, values))
            result = parsed_expression.root.evaluate(assignment)
            index = self.assignment_to_index(values)
            rows.append(TruthRow(values, result, index))

        return TruthTableResult(variables, tuple(rows))

    def from_vector(
        self,
        variables: Tuple[str, ...],
        vector: Iterable[int],
    ) -> TruthTableResult:
        normalized_vector = tuple(int(bool(value)) for value in vector)
        expected_size = 1 << len(variables)

        if len(normalized_vector) != expected_size:
            raise ValueError(
                f"Размер вектора должен быть {expected_size}, получено {len(normalized_vector)}."
            )

        rows = tuple(
            TruthRow(self.index_to_assignment(index, len(variables)), value, index)
            for index, value in enumerate(normalized_vector)
        )
        return TruthTableResult(variables, rows)

    def assignment_to_index(self, assignment: Iterable[int]) -> int:
        index = 0
        for value in assignment:
            index = (index << 1) | int(bool(value))
        return index

    def index_to_assignment(self, index: int, dimension: int) -> Tuple[int, ...]:
        return tuple((index >> bit) & 1 for bit in range(dimension - 1, -1, -1))