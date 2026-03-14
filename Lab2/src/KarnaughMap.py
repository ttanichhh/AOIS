from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

from Lab2.src.Minimization import Minimization, MinimizationResult
from Lab2.src.TruthTable import TruthTable, TruthTableResult


@dataclass(frozen=True)
class KarnaughLayer:
    title: str
    row_labels: Tuple[str, ...]
    col_labels: Tuple[str, ...]
    values: Tuple[Tuple[int, ...], ...]
    indexes: Tuple[Tuple[int, ...], ...]


@dataclass(frozen=True)
class KarnaughMapResult:
    normal_form: str
    expression: str
    selected_implicants: Tuple[str, ...]
    layers: Tuple[KarnaughLayer, ...]
    groups: Tuple[Tuple[int, ...], ...]
    rendered_map: str


class KarnaughMap:
    def minimize(
        self,
        table: TruthTableResult,
        normal_form: str = "sdnf",
    ) -> KarnaughMapResult:
        minimization_result = Minimization().minimize_by_calculation_table(
            table,
            normal_form,
        )
        layers = self.build_layers(table)
        rendered_map = self.render(layers)
        groups = self._groups_from_implicants(table, minimization_result)

        return KarnaughMapResult(
            normal_form=minimization_result.normal_form,
            expression=minimization_result.expression,
            selected_implicants=minimization_result.selected_implicants,
            layers=layers,
            groups=groups,
            rendered_map=rendered_map,
        )

    def build_layers(self, table: TruthTableResult) -> Tuple[KarnaughLayer, ...]:
        if table.dimension == 0:
            return (
                KarnaughLayer(
                    title="const",
                    row_labels=("-",),
                    col_labels=("-",),
                    values=((table.vector[0],),),
                    indexes=((0,),),
                ),
            )

        layer_bits, row_bits, col_bits = self._split_dimension(table.dimension)
        layer_codes = self._gray_codes(layer_bits)
        row_codes = self._gray_codes(row_bits)
        col_codes = self._gray_codes(col_bits)

        layers: List[KarnaughLayer] = []

        for layer_value in layer_codes:
            title = self._build_title(table.variables, layer_value, layer_bits)
            value_rows = []
            index_rows = []

            for row_value in row_codes:
                row_values = []
                row_indexes = []

                for col_value in col_codes:
                    assignment = self._join_bits(
                        layer_value,
                        row_value,
                        col_value,
                        layer_bits,
                        row_bits,
                        col_bits,
                        table.dimension,
                    )
                    index = TruthTable().assignment_to_index(assignment)
                    row_values.append(table.vector[index])
                    row_indexes.append(index)

                value_rows.append(tuple(row_values))
                index_rows.append(tuple(row_indexes))

            layers.append(
                KarnaughLayer(
                    title=title,
                    row_labels=tuple(
                        self._format_label(value, row_bits) for value in row_codes
                    ),
                    col_labels=tuple(
                        self._format_label(value, col_bits) for value in col_codes
                    ),
                    values=tuple(value_rows),
                    indexes=tuple(index_rows),
                )
            )

        return tuple(layers)

    def render(self, layers: Tuple[KarnaughLayer, ...]) -> str:
        lines = []

        for layer in layers:
            lines.append(f"[{layer.title}]")
            lines.append(" " + " ".join(f"{label:>4}" for label in layer.col_labels))
            for row_label, row_values in zip(layer.row_labels, layer.values):
                lines.append(
                    f"{row_label:>3} " + " ".join(f"{value:>4}" for value in row_values)
                )
            lines.append("")

        return "\n".join(lines).rstrip()

    def _groups_from_implicants(
        self,
        table: TruthTableResult,
        minimization_result: MinimizationResult,
    ) -> Tuple[Tuple[int, ...], ...]:
        target_value = 1 if minimization_result.normal_form == "sdnf" else 0
        groups = []
        minimization = Minimization()

        for implicant in minimization_result.selected_implicants:
            covered = tuple(
                index
                for index in range(1 << table.dimension)
                if minimization.implicant_covers_term(
                    implicant,
                    index,
                    table.dimension,
                )
                and table.vector[index] == target_value
            )
            groups.append(covered)

        return tuple(groups)

    def _gray_codes(self, bits: int) -> Tuple[int, ...]:
        if bits == 0:
            return (0,)
        return tuple(index ^ (index >> 1) for index in range(1 << bits))

    def _format_label(self, value: int, bits: int) -> str:
        return "-" if bits == 0 else format(value, f"0{bits}b")

    def _split_dimension(self, dimension: int) -> Tuple[int, int, int]:
        if dimension < 5:
            return 0, max(0, dimension - 2), min(2, dimension)
        return 1, 2, 2

    def _build_title(
        self,
        variables: Tuple[str, ...],
        layer_value: int,
        layer_bits: int,
    ) -> str:
        if layer_bits == 0:
            return "map"

        layer_text = format(layer_value, f"0{layer_bits}b")
        return ", ".join(
            f"{variable}={bit}"
            for variable, bit in zip(variables[:layer_bits], layer_text)
        )

    def _join_bits(
        self,
        layer_value: int,
        row_value: int,
        col_value: int,
        layer_bits: int,
        row_bits: int,
        col_bits: int,
        dimension: int,
    ) -> Tuple[int, ...]:
        layer_text = format(layer_value, f"0{layer_bits}b") if layer_bits else ""
        row_text = format(row_value, f"0{row_bits}b") if row_bits else ""
        col_text = format(col_value, f"0{col_bits}b") if col_bits else ""

        full_text = layer_text + row_text + col_text
        if len(full_text) != dimension:
            full_text = full_text.ljust(dimension, "0")

        return tuple(int(symbol) for symbol in full_text)