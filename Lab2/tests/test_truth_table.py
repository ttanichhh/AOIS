import pytest

from Lab2.src.ExpressionParser import ExpressionParser
from Lab2.src.TruthTable import TruthRow, TruthTable


def test_build_truth_table_for_variable():
    parsed = ExpressionParser().parse("a")
    table = TruthTable().build(parsed)

    assert table.variables == ("a",)
    assert len(table.rows) == 2
    assert table.vector == (0, 1)
    assert table.dimension == 1


def test_build_truth_table_for_constant():
    parsed = ExpressionParser().parse("1")
    table = TruthTable().build(parsed)

    assert table.variables == ()
    assert len(table.rows) == 1
    assert table.rows[0] == TruthRow(tuple(), 1, 0)
    assert table.vector == (1,)


def test_from_vector_builds_rows():
    table = TruthTable().from_vector(("a", "b"), [0, 1, 1, 0])

    assert table.variables == ("a", "b")
    assert len(table.rows) == 4
    assert table.rows[2].assignment == (1, 0)
    assert table.rows[2].result == 1
    assert table.rows[2].index == 2


def test_from_vector_normalizes_values():
    table = TruthTable().from_vector(("a",), [0, 5])
    assert table.vector == (0, 1)


def test_from_vector_invalid_size_raises():
    with pytest.raises(ValueError, match="Размер вектора должен быть 4"):
        TruthTable().from_vector(("a", "b"), [0, 1, 0])


def test_assignment_to_index():
    truth_table = TruthTable()
    assert truth_table.assignment_to_index((0, 0, 0)) == 0
    assert truth_table.assignment_to_index((1, 0, 1)) == 5
    assert truth_table.assignment_to_index((1, 1, 1)) == 7


def test_index_to_assignment():
    truth_table = TruthTable()
    assert truth_table.index_to_assignment(0, 3) == (0, 0, 0)
    assert truth_table.index_to_assignment(5, 3) == (1, 0, 1)
    assert truth_table.index_to_assignment(7, 3) == (1, 1, 1)