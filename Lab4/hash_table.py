from constants import (
    TABLE_SIZE,
    BASE_ADDRESS,
    TABLE_SEPARATOR_WIDTH,
    INDEX_COLUMN_WIDTH,
    KEY_COLUMN_WIDTH,
    DATA_COLUMN_WIDTH,
    VALUE_COLUMN_WIDTH,
    ADDRESS_COLUMN_WIDTH,
    DELETED_CELL_TEXT,
)
from hash_functions import normalize_key, hash_function
from hash_item import HashItem


class HashTable:
    def __init__(self, size=TABLE_SIZE, base_address=BASE_ADDRESS):
        self.size = size
        self.base_address = base_address
        self.count = 0
        self.table = self._create_table()

    def _create_table(self):
        table = []
        for _ in range(self.size):
            table.append(HashItem())
        return table

    def _address_to_index(self, hash_address):
        return hash_address - self.base_address

    def _probe_index(self, start_index, step):
        return (start_index + step) % self.size

    def _find_index_for_key(self, key):
        value, hash_address = hash_function(key, self.size, self.base_address)
        start_index = self._address_to_index(hash_address)

        for step in range(self.size):
            current_index = self._probe_index(start_index, step)
            item = self.table[current_index]

            if item.is_empty():
                return None

            if item.is_active() and item.key == key:
                return current_index

        return None

    def _find_index_for_insert(self, key):
        value, hash_address = hash_function(key, self.size, self.base_address)
        start_index = self._address_to_index(hash_address)
        first_deleted_index = None

        for step in range(self.size):
            current_index = self._probe_index(start_index, step)
            item = self.table[current_index]

            if item.is_active() and item.key == key:
                return None, True, value, hash_address

            if item.is_deleted and first_deleted_index is None:
                first_deleted_index = current_index

            if item.is_empty():
                if first_deleted_index is not None:
                    return first_deleted_index, False, value, hash_address
                return current_index, False, value, hash_address

        if first_deleted_index is not None:
            return first_deleted_index, False, value, hash_address

        return None, False, value, hash_address

    def create(self, key, data):
        normalized_key = normalize_key(key)

        if self.count >= self.size:
            return False, "Таблица переполнена"

        insert_index, duplicate_found, value, hash_address = self._find_index_for_insert(
            normalized_key
        )

        if duplicate_found:
            return False, f"Ключ '{normalized_key}' уже существует"

        if insert_index is None:
            return False, "Не найдено свободное место"

        self.table[insert_index] = HashItem(
            key=normalized_key,
            data=data,
            value=value,
            hash_address=hash_address
        )
        self.count += 1
        return True, "Запись добавлена"

    def read(self, key):
        normalized_key = normalize_key(key)
        index = self._find_index_for_key(normalized_key)

        if index is None:
            return None

        return self.table[index]

    def update(self, key, new_data):
        normalized_key = normalize_key(key)
        index = self._find_index_for_key(normalized_key)

        if index is None:
            return False, f"Ключ '{normalized_key}' не найден"

        self.table[index].data = new_data
        return True, "Запись обновлена"

    def delete(self, key):
        normalized_key = normalize_key(key)
        index = self._find_index_for_key(normalized_key)

        if index is None:
            return False, f"Ключ '{normalized_key}' не найден"

        self.table[index].is_deleted = True
        self.count -= 1
        return True, "Запись удалена"

    def get_fill_factor(self):
        return self.count / self.size

    def print_hash_info(self, key):
        normalized_key = normalize_key(key)
        value, hash_address = hash_function(
            normalized_key,
            self.size,
            self.base_address
        )
        print(f"Ключ: {normalized_key}, V = {value}, h = {hash_address}")

    def _format_item_for_output(self, item):
        if item.is_deleted:
            return (
                DELETED_CELL_TEXT,
                DELETED_CELL_TEXT,
                item.value,
                item.hash_address,
            )

        return item.key, item.data, item.value, item.hash_address

    def print_table(self):
        print("\nХЕШ-ТАБЛИЦА")
        print("-" * TABLE_SEPARATOR_WIDTH)
        print(
            f"{'Индекс':<{INDEX_COLUMN_WIDTH}}"
            f"{'Ключ':<{KEY_COLUMN_WIDTH}}"
            f"{'Данные':<{DATA_COLUMN_WIDTH}}"
            f"{'V':<{VALUE_COLUMN_WIDTH}}"
            f"{'h':<{ADDRESS_COLUMN_WIDTH}}"
            f"{'Удален'}"
        )
        print("-" * TABLE_SEPARATOR_WIDTH)

        for index, item in enumerate(self.table):
            key, data, value, hash_address = self._format_item_for_output(item)
            print(
                f"{index:<{INDEX_COLUMN_WIDTH}}"
                f"{str(key):<{KEY_COLUMN_WIDTH}}"
                f"{str(data):<{DATA_COLUMN_WIDTH}}"
                f"{str(value):<{VALUE_COLUMN_WIDTH}}"
                f"{str(hash_address):<{ADDRESS_COLUMN_WIDTH}}"
                f"{item.is_deleted}"
            )

        print("-" * TABLE_SEPARATOR_WIDTH)
        print(f"Количество записей: {self.count}")
        print(f"Коэффициент заполнения: {self.get_fill_factor():.2f}")
