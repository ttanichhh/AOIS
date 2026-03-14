from __future__ import annotations

from typing import Iterable

from Lab2.src.Analyzer import AnalysisResult
from Lab2.src.Minimization import MinimizationResult, PrimeImplicantChart
from Lab2.src.TruthTable import TruthTableResult


class ReportBuilder:
    def build(self, result: AnalysisResult) -> str:
        lines = [
            f"Формула: {result.parsed_expression.source}",
            "",
            "Таблица истинности:",
            self._format_truth_table(result.truth_table),
            "",
            "СДНФ и СКНФ:",
            f"СДНФ: {result.canonical_forms.sdnf}",
            f"СКНФ: {result.canonical_forms.sknf}",
            f"Числовая форма СДНФ: {result.canonical_forms.sdnf_numeric}",
            f"Числовая форма СКНФ: {result.canonical_forms.sknf_numeric}",
            "",
            "Индексная форма:",
            f"Вектор: {result.canonical_forms.index_vector}",
            f"Индекс: {result.canonical_forms.index_number}",
            "",
            "Классы Поста:",
            self._format_post_classes(result),
            "",
            "Полином Жегалкина:",
            result.zhegalkin_polynomial.expression,
            "",
            "Фиктивные переменные:",
            ", ".join(result.fictitious_variables) if result.fictitious_variables else "нет",
            "",
            "Булевы производные:",
            self._format_derivatives(result),
            "",
        ]

        self._append_calculation_section(
            lines,
            "Минимизация СДНФ (расчетный метод):",
            result.sdnf_calculation_minimization,
        )
        self._append_calculation_section(
            lines,
            "Минимизация СКНФ (расчетный метод):",
            result.sknf_calculation_minimization,
        )
        self._append_calculation_table_section(
            lines,
            "Минимизация СДНФ (расчетно-табличный метод):",
            result.sdnf_calculation_table_minimization,
        )
        self._append_calculation_table_section(
            lines,
            "Минимизация СКНФ (расчетно-табличный метод):",
            result.sknf_calculation_table_minimization,
        )
        self._append_karnaugh_section(
            lines,
            "Минимизация СДНФ (карта Карно):",
            result.sdnf_karnaugh_minimization,
        )
        self._append_karnaugh_section(
            lines,
            "Минимизация СКНФ (карта Карно):",
            result.sknf_karnaugh_minimization,
        )

        return "\n".join(lines).strip()

    def _format_truth_table(self, table: TruthTableResult) -> str:
        header = " ".join(table.variables) + " | f" if table.variables else "f"
        lines = [header, "-" * len(header)]

        for row in table.rows:
            assignment = " ".join(str(value) for value in row.assignment)
            if assignment:
                lines.append(f"{assignment} | {row.result}")
            else:
                lines.append(str(row.result))

        return "\n".join(lines)

    def _format_post_classes(self, result: AnalysisResult) -> str:
        classes = result.post_classes
        return "\n".join(
            [
                f"T0: {'да' if classes.t0 else 'нет'}",
                f"T1: {'да' if classes.t1 else 'нет'}",
                f"S: {'да' if classes.s else 'нет'}",
                f"M: {'да' if classes.m else 'нет'}",
                f"L: {'да' if classes.l else 'нет'}",
            ]
        )

    def _format_derivatives(self, result: AnalysisResult) -> str:
        if not result.derivatives:
            return "нет переменных для дифференциации"

        lines = []
        for derivative in result.derivatives:
            suffix = "".join(derivative.by_variables)
            lines.append(
                f"D_{suffix}: {derivative.sdnf} | индекс={derivative.index_number} ({derivative.index_vector})"
            )

        return "\n".join(lines)

    def _format_gluing_stages(self, result: MinimizationResult) -> str:
        if not result.stages:
            return "склеивание не выполнялось"

        lines = []
        for stage_index, stage in enumerate(result.stages, start=1):
            lines.append(f"Этап {stage_index}:")
            if stage.records:
                for record in stage.records:
                    lines.append(
                        f"  {record.left_pattern} + {record.right_pattern} -> {record.result_pattern}"
                    )
            else:
                lines.append("  нет склеиваемых пар")

            lines.append(f"  Результат: {', '.join(stage.output_patterns)}")

        return "\n".join(lines)

    def _format_redundancy_checks(self, result: MinimizationResult) -> str:
        if result.redundancy_checks:
            return "\n".join(result.redundancy_checks)
        return "нет проверок"

    def _format_chart(self, chart: PrimeImplicantChart | None) -> str:
        if chart is None:
            return "таблица покрытия не построена"

        if not chart.terms:
            return "нет строк для покрытия"

        header = "pat\\idx " + " ".join(f"{term:>3}" for term in chart.terms)
        lines = [header, "-" * len(header)]

        for implicant, row in zip(chart.implicants, chart.matrix):
            row_values = " ".join(f"{cell:>3}" for cell in row)
            lines.append(f"{implicant:>5} {row_values}")

        return "\n".join(lines)

    def _format_implicants(self, patterns: Iterable[str]) -> str:
        values = list(patterns)
        if values:
            return ", ".join(values)
        return "нет"

    def _append_calculation_section(
        self,
        lines: list[str],
        title: str,
        result: MinimizationResult,
    ) -> None:
        lines.extend(
            [
                title,
                f"Исходная {result.form_label}: {result.initial_expression}",
                self._format_gluing_stages(result),
                f"Простые импликанты: {self._format_implicants(result.prime_implicants)}",
                "Проверка лишних термов:",
                self._format_redundancy_checks(result),
                f"Результат: {result.expression}",
                "",
            ]
        )

    def _append_calculation_table_section(
        self,
        lines: list[str],
        title: str,
        result: MinimizationResult,
    ) -> None:
        lines.extend(
            [
                title,
                f"Исходная {result.form_label}: {result.initial_expression}",
                self._format_gluing_stages(result),
                "Таблица покрытия:",
                self._format_chart(result.chart),
                f"Выбранные импликанты: {self._format_implicants(result.selected_implicants)}",
                f"Результат: {result.expression}",
                "",
            ]
        )

    def _append_karnaugh_section(
        self,
        lines: list[str],
        title: str,
        result,
    ) -> None:
        lines.extend(
            [
                title,
                result.rendered_map,
                f"Группы: {result.groups}",
                f"Результат: {result.expression}",
                "",
            ]
        )