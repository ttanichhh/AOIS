import pytest

from Lab2.src.BooleanDerivative import BooleanDerivative
from Lab2.src.TruthTable import TruthTable


def test_find_fictitious_variables():
    table = TruthTable().from_vector(("a", "b"), [0, 0, 1, 1])  # f = a
    fictitious = BooleanDerivative().find_fictitious_variables(table)
    assert fictitious == ("b",)


def test_find_fictitious_variables_for_constant():
    table = TruthTable().from_vector((), [1])
    fictitious = BooleanDerivative().find_fictitious_variables(table)
    assert fictitious == ()


def test_build_first_order_derivative_for_xor():
    table = TruthTable().from_vector(("a", "b"), [0, 1, 1, 0])
    result = BooleanDerivative().build(table, ("a",))

    assert result.by_variables == ("a",)
    assert result.order == 1
    assert result.vector == (1, 1, 1, 1)
    assert result.sdnf == "(!a&!b)|(!a&b)|(a&!b)|(a&b)"
    assert result.numeric_form == (0, 1, 2, 3)
    assert result.index_vector == "1111"
    assert result.index_number == 15


def test_build_second_order_derivative():
    table = TruthTable().from_vector(("a", "b"), [0, 1, 1, 0])
    result = BooleanDerivative().build(table, ("a", "b"))

    assert result.order == 2
    assert result.vector == (0, 0, 0, 0)
    assert result.sdnf == "0"
    assert result.index_number == 0


def test_build_all_derivatives():
    table = TruthTable().from_vector(("a", "b", "c"), [0, 1, 1, 0, 1, 0, 0, 1])
    results = BooleanDerivative().build_all(table, max_order=2)

    names = {r.by_variables for r in results}
    assert names == {
        ("a",), ("b",), ("c",),
        ("a", "b"), ("a", "c"), ("b", "c"),
    }


def test_build_all_derivatives_respects_dimension():
    table = TruthTable().from_vector(("a",), [0, 1])
    results = BooleanDerivative().build_all(table, max_order=4)
    assert len(results) == 1
    assert results[0].by_variables == ("a",)


def test_build_derivative_requires_variable():
    table = TruthTable().from_vector(("a",), [0, 1])
    with pytest.raises(ValueError, match="хотя бы одна переменная"):
        BooleanDerivative().build(table, tuple())


def test_build_derivative_unknown_variable_raises():
    table = TruthTable().from_vector(("a",), [0, 1])
    with pytest.raises(ValueError, match="Неизвестные переменные"):
        BooleanDerivative().build(table, ("b",))