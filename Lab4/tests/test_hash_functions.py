import pytest

from constants import ALPHABET_BASE
from hash_functions import (
    get_letter_value,
    hash_function,
    key_to_value,
    normalize_key,
    validate_key,
)


def test_normalize_key_strips_spaces_and_uppercases():
    assert normalize_key("  атом ") == "АТОМ"


def test_validate_key_raises_for_empty_values():
    with pytest.raises(ValueError, match="Ключ не может быть пустым"):
        validate_key("")

    with pytest.raises(ValueError, match="Ключ не может быть пустым"):
        validate_key(None)


def test_get_letter_value_returns_index_for_russian_letter():
    assert get_letter_value("А") == 0
    assert get_letter_value("Я") == 32


def test_get_letter_value_raises_for_invalid_symbol():
    with pytest.raises(ValueError, match="не входит в русский алфавит"):
        get_letter_value("A")


def test_key_to_value_uses_first_two_letters_only():
    assert key_to_value("атом") == 0 * ALPHABET_BASE + 19


def test_key_to_value_uses_zero_for_missing_second_letter():
    assert key_to_value("Я") == 32 * ALPHABET_BASE


def test_hash_function_returns_value_and_shifted_address():
    value, hash_address = hash_function("Ток", table_size=20, base_address=100)

    assert value == key_to_value("Ток")
    assert hash_address == (value % 20) + 100
