import pytest

from Lab2.src.PostClasses import PostClasses
from Lab2.src.TruthTable import TruthTable, TruthTableResult


def test_post_classes_for_and():
    table = TruthTable().from_vector(("a", "b"), [0, 0, 0, 1])
    result = PostClasses().determine(table)

    assert result.t0 is True
    assert result.t1 is True
    assert result.s is False
    assert result.m is True
    assert result.l is False


def test_post_classes_for_xor():
    table = TruthTable().from_vector(("a", "b"), [0, 1, 1, 0])
    result = PostClasses().determine(table)

    assert result.t0 is True
    assert result.t1 is False
    assert result.s is False
    assert result.m is False
    assert result.l is True


def test_post_classes_for_not_a():
    table = TruthTable().from_vector(("a",), [1, 0])
    result = PostClasses().determine(table)

    assert result.s is True


def test_determine_raises_on_empty_rows():
    empty_table = TruthTableResult(variables=("a",), rows=tuple())
    with pytest.raises(ValueError, match="Таблица истинности пуста"):
        PostClasses().determine(empty_table)