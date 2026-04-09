from io import StringIO
from contextlib import redirect_stdout

from hash_table import HashTable


class TestHashTable:
    def test_create_table_initializes_with_empty_items(self):
        table = HashTable(size=3, base_address=10)

        assert len(table.table) == 3
        assert table.count == 0
        assert all(item.is_empty() for item in table.table)

    def test_address_to_index_and_probe_index(self):
        table = HashTable(size=5, base_address=10)

        assert table._address_to_index(12) == 2
        assert table._probe_index(4, 2) == 1

    def test_create_and_read_record(self):
        table = HashTable(size=5)

        success, message = table.create(" атом ", "Наименьшая частица")
        record = table.read("атом")

        assert success is True
        assert message == "Запись добавлена"
        assert record is not None
        assert record.key == "АТОМ"
        assert record.data == "Наименьшая частица"
        assert record.value is not None
        assert record.hash_address is not None
        assert table.count == 1

    def test_read_returns_none_for_missing_key(self):
        table = HashTable(size=5)

        assert table.read("ФОТОН") is None

    def test_duplicate_key_is_rejected(self):
        table = HashTable(size=5)
        table.create("АТОМ", "one")

        success, message = table.create("атом", "two")

        assert success is False
        assert message == "Ключ 'АТОМ' уже существует"
        assert table.count == 1

    def test_update_changes_existing_record(self):
        table = HashTable(size=5)
        table.create("ТОК", "старое")

        success, message = table.update("ток", "новое")

        assert success is True
        assert message == "Запись обновлена"
        assert table.read("ТОК").data == "новое"

    def test_update_returns_error_for_missing_key(self):
        table = HashTable(size=5)

        success, message = table.update("ТОК", "новое")

        assert success is False
        assert message == "Ключ 'ТОК' не найден"

    def test_delete_marks_record_as_deleted(self):
        table = HashTable(size=5)
        table.create("ПОЛЕ", "данные")

        success, message = table.delete("поле")

        assert success is True
        assert message == "Запись удалена"
        assert table.read("ПОЛЕ") is None
        assert table.count == 0
        assert any(item.is_deleted for item in table.table)

    def test_delete_returns_error_for_missing_key(self):
        table = HashTable(size=5)

        success, message = table.delete("ПОЛЕ")

        assert success is False
        assert message == "Ключ 'ПОЛЕ' не найден"

    def test_deleted_slot_is_reused_for_new_record(self):
        table = HashTable(size=2)
        table.create("АА", "first")
        table.create("ББ", "second")
        table.delete("АА")

        success, message = table.create("ВВ", "third")
        record = table.read("ВВ")

        assert success is True
        assert message == "Запись добавлена"
        assert record is not None
        assert table.count == 2

    def test_create_returns_table_overflow_when_count_reaches_size(self):
        table = HashTable(size=1)
        table.create("АА", "first")

        success, message = table.create("ББ", "second")

        assert success is False
        assert message == "Таблица переполнена"

    def test_find_index_for_insert_detects_duplicate_and_returns_hash_data(self):
        table = HashTable(size=5)
        table.create("АА", "first")

        index, duplicate_found, value, hash_address = table._find_index_for_insert("АА")

        assert index is None
        assert duplicate_found is True
        assert value == 0
        assert hash_address == 0

    def test_find_index_for_key_stops_on_empty_slot(self):
        table = HashTable(size=5)

        assert table._find_index_for_key("АА") is None

    def test_linear_probing_finds_next_slot_for_collision(self):
        table = HashTable(size=3)
        table.create("АА", "first")

        insert_index, duplicate_found, _, _ = table._find_index_for_insert("АГ")

        assert duplicate_found is False
        assert insert_index == 1

    def test_find_index_for_insert_returns_none_when_only_active_items_exist(self):
        table = HashTable(size=2)
        table.create("АА", "first")
        table.create("АБ", "second")
        table.count = 0

        insert_index, duplicate_found, _, _ = table._find_index_for_insert("АВ")

        assert insert_index is None
        assert duplicate_found is False

    def test_get_fill_factor(self):
        table = HashTable(size=4)
        table.create("АА", "first")
        table.create("АБ", "second")

        assert table.get_fill_factor() == 0.5

    def test_print_hash_info_outputs_expected_text(self):
        table = HashTable(size=20)
        buffer = StringIO()

        with redirect_stdout(buffer):
            table.print_hash_info(" ток ")

        output = buffer.getvalue()
        assert "Ключ: ТОК" in output
        assert "V = 642" in output
        assert "h = 2" in output

    def test_print_table_outputs_summary(self):
        table = HashTable(size=2)
        table.create("АА", "first")
        buffer = StringIO()

        with redirect_stdout(buffer):
            table.print_table()

        output = buffer.getvalue()
        assert "ХЕШ-ТАБЛИЦА" in output
        assert "Количество записей: 1" in output
        assert "Коэффициент заполнения: 0.50" in output
        assert "АА" in output

    def test_print_table_formats_deleted_record_as_deleted_text(self):
        table = HashTable(size=3)
        table.create("АА", "first")
        table.delete("АА")
        buffer = StringIO()

        with redirect_stdout(buffer):
            table.print_table()

        output = buffer.getvalue()
        assert "<удалено>" in output
        assert "True" in output
