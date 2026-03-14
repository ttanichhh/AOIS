from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence, Tuple

from Lab2.src.CanonicalForms import CanonicalForms
from Lab2.src.TruthTable import TruthTableResult


SUPPORTED_FORMS = {"sdnf", "sknf"}


@dataclass(frozen=True)
class Implicant:
    pattern: str
    indexes: Tuple[int, ...]

    @property
    def literals_count(self) -> int:
        return sum(1 for symbol in self.pattern if symbol != "-")


@dataclass(frozen=True)
class GluingRecord:
    left_pattern: str
    right_pattern: str
    result_pattern: str


@dataclass(frozen=True)
class GluingStage:
    input_patterns: Tuple[str, ...]
    records: Tuple[GluingRecord, ...]
    output_patterns: Tuple[str, ...]


@dataclass(frozen=True)
class PrimeImplicantChart:
    terms: Tuple[int, ...]
    implicants: Tuple[str, ...]
    matrix: Tuple[Tuple[int, ...], ...]
    normal_form: str


@dataclass(frozen=True)
class MinimizationResult:
    method_name: str
    normal_form: str
    initial_expression: str
    stages: Tuple[GluingStage, ...]
    prime_implicants: Tuple[str, ...]
    selected_implicants: Tuple[str, ...]
    expression: str
    redundancy_checks: Tuple[str, ...] = tuple()
    chart: PrimeImplicantChart | None = None

    @property
    def form_label(self) -> str:
        return "СДНФ" if self.normal_form == "sdnf" else "СКНФ"


class Minimization:
    def minimize_by_calculation(
        self,
        table: TruthTableResult,
        normal_form: str = "sdnf",
    ) -> MinimizationResult:
        normalized_form = self._normalize_form(normal_form)
        terms, initial_expression = self._extract_terms(table, normalized_form)

        if not terms:
            return MinimizationResult(
                method_name="calculation",
                normal_form=normalized_form,
                initial_expression=initial_expression,
                stages=tuple(),
                prime_implicants=tuple(),
                selected_implicants=tuple(),
                expression="0" if normalized_form == "sdnf" else "1",
            )

        stages, prime_implicants = self._generate_prime_implicants(
            table.dimension,
            terms,
        )
        selected = [item.pattern for item in prime_implicants]
        checks = []

        for pattern in list(selected):
            other_patterns = [value for value in selected if value != pattern]
            removable = self._can_remove_pattern(
                pattern,
                other_patterns,
                terms,
                table.dimension,
            )

            if removable:
                checks.append(f"{pattern}: удалена как лишняя")
                selected.remove(pattern)
            else:
                checks.append(f"{pattern}: оставлена")

        selected.sort(
            key=lambda pattern: (sum(bit != "-" for bit in pattern), pattern)
        )

        return MinimizationResult(
            method_name="calculation",
            normal_form=normalized_form,
            initial_expression=initial_expression,
            stages=stages,
            prime_implicants=tuple(item.pattern for item in prime_implicants),
            selected_implicants=tuple(selected),
            expression=self._patterns_to_expression(
                selected,
                table.variables,
                normalized_form,
            ),
            redundancy_checks=tuple(checks),
        )

    def minimize_by_calculation_table(
        self,
        table: TruthTableResult,
        normal_form: str = "sdnf",
    ) -> MinimizationResult:
        normalized_form = self._normalize_form(normal_form)
        terms, initial_expression = self._extract_terms(table, normalized_form)

        if not terms:
            return MinimizationResult(
                method_name="calculation_table",
                normal_form=normalized_form,
                initial_expression=initial_expression,
                stages=tuple(),
                prime_implicants=tuple(),
                selected_implicants=tuple(),
                expression="0" if normalized_form == "sdnf" else "1",
                chart=PrimeImplicantChart(
                    tuple(),
                    tuple(),
                    tuple(),
                    normalized_form,
                ),
            )

        stages, prime_implicants = self._generate_prime_implicants(
            table.dimension,
            terms,
        )
        prime_patterns = [item.pattern for item in prime_implicants]
        prime_patterns.sort(
            key=lambda pattern: (sum(bit != "-" for bit in pattern), pattern)
        )

        chart = self._build_chart(
            table.dimension,
            prime_patterns,
            terms,
            normalized_form,
        )
        selected = self._select_covering_implicants(chart, table.dimension)

        return MinimizationResult(
            method_name="calculation_table",
            normal_form=normalized_form,
            initial_expression=initial_expression,
            stages=stages,
            prime_implicants=tuple(prime_patterns),
            selected_implicants=tuple(selected),
            expression=self._patterns_to_expression(
                selected,
                table.variables,
                normalized_form,
            ),
            chart=chart,
        )

    def implicant_covers_term(
        self,
        pattern: str,
        index: int,
        dimension: int,
    ) -> bool:
        candidate = format(index, f"0{dimension}b")
        return all(
            symbol == "-" or symbol == bit
            for symbol, bit in zip(pattern, candidate)
        )

    def _normalize_form(self, normal_form: str) -> str:
        normalized = normal_form.lower()
        if normalized not in SUPPORTED_FORMS:
            raise ValueError(f"Неподдерживаемая форма: {normal_form}")
        return normalized

    def _extract_terms(
        self,
        table: TruthTableResult,
        normal_form: str,
    ) -> Tuple[Tuple[int, ...], str]:
        canonical = CanonicalForms().build(table)
        if normal_form == "sdnf":
            return canonical.sdnf_numeric, canonical.sdnf
        return canonical.sknf_numeric, canonical.sknf

    def _generate_prime_implicants(
        self,
        dimension: int,
        terms: Sequence[int],
    ) -> Tuple[Tuple[GluingStage, ...], Tuple[Implicant, ...]]:
        current = self._merge_duplicate_implicants(
            Implicant(format(index, f"0{dimension}b"), (index,))
            for index in sorted(set(terms))
        )

        stages = []
        prime_map: Dict[str, set[int]] = {}

        while current:
            groups: Dict[int, List[Implicant]] = {}
            for implicant in current:
                ones_count = implicant.pattern.count("1")
                groups.setdefault(ones_count, []).append(implicant)

            used_patterns = set()
            next_implicants = []
            records: Dict[Tuple[str, str, str], GluingRecord] = {}

            for group_index in sorted(groups):
                left_group = groups.get(group_index, [])
                right_group = groups.get(group_index + 1, [])

                for left_implicant in left_group:
                    for right_implicant in right_group:
                        combined_pattern = self._combine_patterns(
                            left_implicant.pattern,
                            right_implicant.pattern,
                        )
                        if combined_pattern is None:
                            continue

                        used_patterns.add(left_implicant.pattern)
                        used_patterns.add(right_implicant.pattern)

                        merged_indexes = tuple(
                            sorted(
                                set(left_implicant.indexes)
                                | set(right_implicant.indexes)
                            )
                        )
                        next_implicants.append(
                            Implicant(combined_pattern, merged_indexes)
                        )

                        record_key = (
                            min(
                                left_implicant.pattern,
                                right_implicant.pattern,
                            ),
                            max(
                                left_implicant.pattern,
                                right_implicant.pattern,
                            ),
                            combined_pattern,
                        )
                        records[record_key] = GluingRecord(
                            left_pattern=record_key[0],
                            right_pattern=record_key[1],
                            result_pattern=combined_pattern,
                        )

            for implicant in current:
                if implicant.pattern not in used_patterns:
                    prime_map.setdefault(implicant.pattern, set()).update(
                        implicant.indexes
                    )

            if not next_implicants:
                break

            next_merged = self._merge_duplicate_implicants(next_implicants)
            stages.append(
                GluingStage(
                    input_patterns=tuple(item.pattern for item in current),
                    records=tuple(records[key] for key in sorted(records)),
                    output_patterns=tuple(item.pattern for item in next_merged),
                )
            )
            current = next_merged

        prime_result = self._merge_duplicate_implicants(
            Implicant(pattern=pattern, indexes=tuple(sorted(indexes)))
            for pattern, indexes in prime_map.items()
        )

        return tuple(stages), tuple(prime_result)

    def _combine_patterns(self, left: str, right: str) -> str | None:
        differences = 0
        result = []

        for left_symbol, right_symbol in zip(left, right):
            if left_symbol == right_symbol:
                result.append(left_symbol)
                continue
            if left_symbol == "-" or right_symbol == "-":
                return None
            differences += 1
            result.append("-")
            if differences > 1:
                return None

        if differences != 1:
            return None
        return "".join(result)

    def _merge_duplicate_implicants(
        self,
        implicants: Iterable[Implicant],
    ) -> List[Implicant]:
        merged: Dict[str, set[int]] = {}
        for implicant in implicants:
            merged.setdefault(implicant.pattern, set()).update(implicant.indexes)

        result = [
            Implicant(pattern=pattern, indexes=tuple(sorted(indexes)))
            for pattern, indexes in merged.items()
        ]
        result.sort(key=lambda item: (item.literals_count, item.pattern))
        return result

    def _can_remove_pattern(
        self,
        pattern: str,
        other_patterns: Sequence[str],
        terms: Sequence[int],
        dimension: int,
    ) -> bool:
        for term in terms:
            if self.implicant_covers_term(pattern, term, dimension):
                if not any(
                    self.implicant_covers_term(other, term, dimension)
                    for other in other_patterns
                ):
                    return False
        return True

    def _pattern_to_term(
        self,
        pattern: str,
        variables: Tuple[str, ...],
        normal_form: str,
    ) -> str:
        literals = []

        for bit, variable in zip(pattern, variables):
            if normal_form == "sdnf":
                if bit == "1":
                    literals.append(variable)
                elif bit == "0":
                    literals.append(f"!{variable}")
            else:
                if bit == "0":
                    literals.append(variable)
                elif bit == "1":
                    literals.append(f"!{variable}")

        if not literals:
            return "1" if normal_form == "sdnf" else "0"

        joiner = "&" if normal_form == "sdnf" else "|"
        return literals[0] if len(literals) == 1 else f"({joiner.join(literals)})"

    def _patterns_to_expression(
        self,
        patterns: Sequence[str],
        variables: Tuple[str, ...],
        normal_form: str,
    ) -> str:
        if not patterns:
            return "0" if normal_form == "sdnf" else "1"

        terms = [
            self._pattern_to_term(pattern, variables, normal_form)
            for pattern in patterns
        ]
        joiner = "|" if normal_form == "sdnf" else "&"
        return joiner.join(terms)

    def _build_chart(
        self,
        dimension: int,
        prime_patterns: Sequence[str],
        terms: Sequence[int],
        normal_form: str,
    ) -> PrimeImplicantChart:
        matrix = tuple(
            tuple(
                int(self.implicant_covers_term(pattern, term, dimension))
                for term in terms
            )
            for pattern in prime_patterns
        )

        return PrimeImplicantChart(
            terms=tuple(terms),
            implicants=tuple(prime_patterns),
            matrix=matrix,
            normal_form=normal_form,
        )

    def _select_covering_implicants(
        self,
        chart: PrimeImplicantChart,
        dimension: int,
    ) -> Tuple[str, ...]:
        selected = set()

        for column_index, _ in enumerate(chart.terms):
            covering = [
                chart.implicants[row_index]
                for row_index, row in enumerate(chart.matrix)
                if row[column_index] == 1
            ]
            if len(covering) == 1:
                selected.add(covering[0])

        uncovered = set(chart.terms)
        for pattern in selected:
            for term in chart.terms:
                if self.implicant_covers_term(pattern, term, dimension):
                    uncovered.discard(term)

        while uncovered:
            candidates = [
                pattern
                for pattern in chart.implicants
                if pattern not in selected
            ]
            scores = []

            for pattern in candidates:
                covered_terms = {
                    term
                    for term in uncovered
                    if self.implicant_covers_term(pattern, term, dimension)
                }
                scores.append(
                    (
                        len(covered_terms),
                        -sum(bit != "-" for bit in pattern),
                        pattern,
                        covered_terms,
                    )
                )

            scores.sort(reverse=True)
            best_cover_count, _, best_pattern, covered_terms = scores[0]
            if best_cover_count == 0:
                break

            selected.add(best_pattern)
            uncovered -= covered_terms

        result = sorted(
            selected,
            key=lambda pattern: (sum(bit != "-" for bit in pattern), pattern),
        )
        return tuple(result)