from constants import RUS_ALPHABET, ALPHABET_BASE


def normalize_key(key):
    return key.strip().upper()


def validate_key(key):
    if not key:
        raise ValueError("Ключ не может быть пустым")


def get_letter_value(letter):
    if letter not in RUS_ALPHABET:
        raise ValueError(f"Символ '{letter}' не входит в русский алфавит")
    return RUS_ALPHABET[letter]


def key_to_value(key):
    normalized_key = normalize_key(key)
    validate_key(normalized_key)

    first_value = get_letter_value(normalized_key[0])

    if len(normalized_key) > 1:
        second_value = get_letter_value(normalized_key[1])
    else:
        second_value = 0

    return first_value * ALPHABET_BASE + second_value


def hash_function(key, table_size, base_address):
    value = key_to_value(key)
    hash_address = (value % table_size) + base_address
    return value, hash_address