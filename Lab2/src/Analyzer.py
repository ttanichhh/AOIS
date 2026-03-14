from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from Lab2.src.BooleanDerivative import BooleanDerivative, BooleanDerivativeResult
from Lab2.src.CanonicalForms import CanonicalForms, CanonicalFormsResult
from Lab2.src.ExpressionParser import ExpressionParser, ParsedExpression
from Lab2.src.KarnaughMap import KarnaughMap, KarnaughMapResult
from Lab2.src.Minimization import Minimization, MinimizationResult
from Lab2.src.PostClasses import PostClasses, PostClassesResult
from Lab2.src.TruthTable import TruthTable, TruthTableResult
from Lab2.src.ZhegalkinPolynomial import ZhegalkinPolynomial, ZhegalkinPolynomialResult


@dataclass(frozen=True)
class AnalysisResult:
    parsed_expression: ParsedExpression
    truth_table: TruthTableResult
    canonical_forms: CanonicalFormsResult
    post_classes: PostClassesResult
    zhegalkin_polynomial: ZhegalkinPolynomialResult
    fictitious_variables: Tuple[str, ...]
    derivatives: Tuple[BooleanDerivativeResult, ...]
    sdnf_calculation_minimization: MinimizationResult
    sdnf_calculation_table_minimization: MinimizationResult
    sdnf_karnaugh_minimization: KarnaughMapResult
    sknf_calculation_minimization: MinimizationResult
    sknf_calculation_table_minimization: MinimizationResult
    sknf_karnaugh_minimization: KarnaughMapResult


class Analyzer:
    def analyze(self, source: str) -> AnalysisResult:
        parsed_expression = ExpressionParser().parse(source)
        truth_table = TruthTable().build(parsed_expression)
        canonical_forms = CanonicalForms().build(truth_table)
        post_classes = PostClasses().determine(truth_table)
        zhegalkin_polynomial = ZhegalkinPolynomial().build(truth_table)

        derivative_service = BooleanDerivative()
        fictitious_variables = derivative_service.find_fictitious_variables(
            truth_table
        )
        derivatives = derivative_service.build_all(truth_table)

        minimization_service = Minimization()
        karnaugh_service = KarnaughMap()

        sdnf_calculation_minimization = (
            minimization_service.minimize_by_calculation(
                truth_table,
                "sdnf",
            )
        )
        sdnf_calculation_table_minimization = (
            minimization_service.minimize_by_calculation_table(
                truth_table,
                "sdnf",
            )
        )
        sdnf_karnaugh_minimization = karnaugh_service.minimize(
            truth_table,
            "sdnf",
        )

        sknf_calculation_minimization = (
            minimization_service.minimize_by_calculation(
                truth_table,
                "sknf",
            )
        )
        sknf_calculation_table_minimization = (
            minimization_service.minimize_by_calculation_table(
                truth_table,
                "sknf",
            )
        )
        sknf_karnaugh_minimization = karnaugh_service.minimize(
            truth_table,
            "sknf",
        )

        return AnalysisResult(
            parsed_expression=parsed_expression,
            truth_table=truth_table,
            canonical_forms=canonical_forms,
            post_classes=post_classes,
            zhegalkin_polynomial=zhegalkin_polynomial,
            fictitious_variables=fictitious_variables,
            derivatives=derivatives,
            sdnf_calculation_minimization=sdnf_calculation_minimization,
            sdnf_calculation_table_minimization=sdnf_calculation_table_minimization,
            sdnf_karnaugh_minimization=sdnf_karnaugh_minimization,
            sknf_calculation_minimization=sknf_calculation_minimization,
            sknf_calculation_table_minimization=sknf_calculation_table_minimization,
            sknf_karnaugh_minimization=sknf_karnaugh_minimization,
        )