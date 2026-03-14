import pytest

from Lab2.src.ExpressionParser import (
    BinaryNode,
    ConstantNode,
    ExpressionParser,
    UnaryNode,
    VariableNode,
)


def test_parse_variable():
    parsed = ExpressionParser().parse("a")
    assert parsed.source == "a"
    assert parsed.variables == ("a",)
    assert isinstance(parsed.root, VariableNode)


def test_parse_constant():
    parsed = ExpressionParser().parse("1")
    assert parsed.variables == ()
    assert isinstance(parsed.root, ConstantNode)
    assert parsed.root.evaluate({}) == 1


def test_parse_unary_and_binary_expression():
    parsed = ExpressionParser().parse("!(a&b)|c")
    assert parsed.variables == ("a", "b", "c")
    assert isinstance(parsed.root, BinaryNode)


def test_parse_implication_is_right_associative():
    parsed = ExpressionParser().parse("a->b->c")
    assert parsed.variables == ("a", "b", "c")
    assert parsed.root.evaluate({"a": 1, "b": 1, "c": 0}) == 0


def test_parse_equivalence():
    parsed = ExpressionParser().parse("a~b")
    assert parsed.variables == ("a", "b")
    assert parsed.root.evaluate({"a": 1, "b": 1}) == 1
    assert parsed.root.evaluate({"a": 1, "b": 0}) == 0


def test_symbol_normalization():
    parsed = ExpressionParser().parse("¬a ∨ (b ∧ c) → d ↔ e")
    assert parsed.source == "!a | (b & c) -> d ~ e"
    assert parsed.variables == ("a", "b", "c", "d", "e")


def test_parse_with_underscore_and_digits():
    parsed = ExpressionParser().parse("x_1&y2")
    assert parsed.variables == ("x_1", "y2")


def test_empty_formula_raises():
    with pytest.raises(ValueError, match="Формула не должна быть пустой"):
        ExpressionParser().parse("   ")


def test_invalid_symbol_raises():
    with pytest.raises(ValueError, match="Недопустимый символ"):
        ExpressionParser().parse("a+b")


def test_missing_right_parenthesis_raises():
    with pytest.raises(ValueError, match="Ожидался токен RPAREN"):
        ExpressionParser().parse("(a&b")


def test_invalid_primary_raises():
    with pytest.raises(ValueError, match="Ожидалась переменная, константа или '\\('"):
        ExpressionParser().parse("&a")


def test_more_than_max_variables_raises():
    with pytest.raises(ValueError, match="Поддерживается не более 5 переменных"):
        ExpressionParser().parse("a&b&c&d&e&f")


def test_variable_node_missing_value_raises():
    node = VariableNode("x")
    with pytest.raises(ValueError, match="не задано значение"):
        node.evaluate({})


def test_unary_unknown_operator_raises():
    node = UnaryNode("?", ConstantNode(1))
    with pytest.raises(ValueError, match="Неизвестный унарный оператор"):
        node.evaluate({})


def test_binary_unknown_operator_raises():
    node = BinaryNode("?", ConstantNode(1), ConstantNode(0))
    with pytest.raises(ValueError, match="Неизвестный бинарный оператор"):
        node.evaluate({})


def test_collect_variables():
    parsed = ExpressionParser().parse("(z&a)|!m")
    assert parsed.variables == ("a", "m", "z")