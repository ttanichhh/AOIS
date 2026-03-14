from Lab2.src.CanonicalForms import CanonicalForms
from Lab2.src.TruthTable import TruthTable


def test_build_canonical_forms_for_xor():
    table = TruthTable().from_vector(("a", "b"), [0, 1, 1, 0])
    result = CanonicalForms().build(table)

    assert result.sdnf == "(!a&b)|(a&!b)"
    assert result.sknf == "(a|b)&(!a|!b)"
    assert result.sdnf_numeric == (1, 2)
    assert result.sknf_numeric == (0, 3)
    assert result.index_vector == "0110"
    assert result.index_number == 6


def test_build_canonical_forms_all_zero():
    table = TruthTable().from_vector(("a",), [0, 0])
    result = CanonicalForms().build(table)

    assert result.sdnf == "0"
    assert result.sknf == "a&!a"
    assert result.sdnf_numeric == ()
    assert result.sknf_numeric == (0, 1)


def test_build_canonical_forms_all_one():
    table = TruthTable().from_vector(("a",), [1, 1])
    result = CanonicalForms().build(table)

    assert result.sdnf == "!a|a"
    assert result.sknf == "1"
    assert result.sknf_numeric == ()
    assert result.sdnf_numeric == (0, 1)


def test_build_canonical_forms_for_constant_one():
    table = TruthTable().from_vector((), [1])
    result = CanonicalForms().build(table)

    assert result.sdnf == "1"
    assert result.sknf == "1"
    assert result.index_vector == "1"
    assert result.index_number == 1


def test_build_canonical_forms_for_constant_zero():
    table = TruthTable().from_vector((), [0])
    result = CanonicalForms().build(table)

    assert result.sdnf == "0"
    assert result.sknf == "0"
    assert result.index_vector == "0"
    assert result.index_number == 0