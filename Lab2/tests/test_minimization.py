import pytest

from Lab2.src.Minimization import Minimization
from Lab2.src.TruthTable import TruthTable


def test_minimize_by_calculation_sdnf():
    table = TruthTable().from_vector(("a", "b"), [0, 0, 1, 1])  # f = a
    result = Minimization().minimize_by_calculation(table, "sdnf")

    assert result.method_name == "calculation"
    assert result.normal_form == "sdnf"
    assert result.initial_expression == "(a&!b)|(a&b)"
    assert result.expression == "a"
    assert result.prime_implicants == ("1-",)
    assert result.selected_implicants == ("1-",)
    assert result.form_label == "СДНФ"
    assert len(result.stages) == 1
    assert "оставлена" in result.redundancy_checks[0]


def test_minimize_by_calculation_sknf():
    table = TruthTable().from_vector(("a", "b"), [0, 0, 1, 1])  # f = a
    result = Minimization().minimize_by_calculation(table, "sknf")

    assert result.normal_form == "sknf"
    assert result.expression == "a"
    assert result.form_label == "СКНФ"


def test_minimize_by_calculation_no_terms_for_sdnf():
    table = TruthTable().from_vector(("a",), [0, 0])
    result = Minimization().minimize_by_calculation(table, "sdnf")

    assert result.expression == "0"
    assert result.prime_implicants == ()
    assert result.selected_implicants == ()
    assert result.stages == ()


def test_minimize_by_calculation_no_terms_for_sknf():
    table = TruthTable().from_vector(("a",), [1, 1])
    result = Minimization().minimize_by_calculation(table, "sknf")

    assert result.expression == "1"
    assert result.prime_implicants == ()
    assert result.selected_implicants == ()


def test_minimize_by_calculation_table_sdnf():
    table = TruthTable().from_vector(("a", "b"), [0, 1, 1, 1])  # a|b
    result = Minimization().minimize_by_calculation_table(table, "sdnf")

    assert result.method_name == "calculation_table"
    assert result.normal_form == "sdnf"
    assert result.expression in {"a|b", "b|a"}
    assert result.chart is not None
    assert result.chart.terms == (1, 2, 3)
    assert set(result.selected_implicants) == {"-1", "1-"}


def test_minimize_by_calculation_table_no_terms():
    table = TruthTable().from_vector(("a",), [0, 0])
    result = Minimization().minimize_by_calculation_table(table, "sdnf")

    assert result.expression == "0"
    assert result.chart is not None
    assert result.chart.terms == ()
    assert result.chart.matrix == ()


def test_implicant_covers_term():
    m = Minimization()
    assert m.implicant_covers_term("1-", 2, 2) is True
    assert m.implicant_covers_term("1-", 3, 2) is True
    assert m.implicant_covers_term("1-", 1, 2) is False


def test_invalid_normal_form_raises():
    table = TruthTable().from_vector(("a",), [0, 1])
    with pytest.raises(ValueError, match="Неподдерживаемая форма"):
        Minimization().minimize_by_calculation(table, "abc")