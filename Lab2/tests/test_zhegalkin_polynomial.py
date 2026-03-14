from Lab2.src.TruthTable import TruthTable
from Lab2.src.ZhegalkinPolynomial import ZhegalkinPolynomial


def test_zhegalkin_for_xor():
    table = TruthTable().from_vector(("a", "b"), [0, 1, 1, 0])
    result = ZhegalkinPolynomial().build(table)

    assert result.coefficients == (0, 1, 1, 0)
    assert result.monomials == ("b", "a")
    assert result.expression == "b ^ a"


def test_zhegalkin_for_constant_zero():
    table = TruthTable().from_vector((), [0])
    result = ZhegalkinPolynomial().build(table)

    assert result.coefficients == (0,)
    assert result.monomials == ()
    assert result.expression == "0"


def test_zhegalkin_for_constant_one():
    table = TruthTable().from_vector((), [1])
    result = ZhegalkinPolynomial().build(table)

    assert result.coefficients == (1,)
    assert result.monomials == ("1",)
    assert result.expression == "1"


def test_mask_to_monomial_order():
    table = TruthTable().from_vector(("a", "b", "c"), [0] * 8)
    poly = ZhegalkinPolynomial()
    coeffs = poly.coefficients(table)
    assert coeffs == (0, 0, 0, 0, 0, 0, 0, 0)