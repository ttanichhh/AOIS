from Lab2.src.Analyzer import Analyzer


def test_analyzer_returns_full_result():
    result = Analyzer().analyze("a|b")

    assert result.parsed_expression.source == "a|b"
    assert result.truth_table.variables == ("a", "b")
    assert result.canonical_forms.index_vector == "0111"
    assert result.post_classes.t0 is True
    assert result.zhegalkin_polynomial.expression == "b ^ a ^ a*b"
    assert isinstance(result.fictitious_variables, tuple)
    assert isinstance(result.derivatives, tuple)

    assert result.sdnf_calculation_minimization.expression in {"a|b", "b|a"}
    assert result.sdnf_calculation_table_minimization.expression in {"a|b", "b|a"}
    assert result.sdnf_karnaugh_minimization.expression in {"a|b", "b|a"}

    assert result.sknf_calculation_minimization.expression == "(a|b)"
    assert result.sknf_calculation_table_minimization.expression == "(a|b)"
    assert result.sknf_karnaugh_minimization.expression == "(a|b)"