from contextlib import redirect_stdout
from io import StringIO

import main
from hash_item import HashItem
from hash_table import HashTable


def test_print_result_prints_success_message():
    buffer = StringIO()

    with redirect_stdout(buffer):
        main.print_result(True, "ok")

    assert buffer.getvalue().strip() == "Успех: ok"


def test_print_result_prints_error_message():
    buffer = StringIO()

    with redirect_stdout(buffer):
        main.print_result(False, "fail")

    assert buffer.getvalue().strip() == "Ошибка: fail"


def test_print_record_handles_missing_record():
    buffer = StringIO()

    with redirect_stdout(buffer):
        main.print_record(None)

    assert buffer.getvalue().strip() == "Запись не найдена"


def test_print_record_prints_all_fields():
    record = HashItem(key="ИВАНОВ", data="Илья, баскетбол", value=321, hash_address=1)
    buffer = StringIO()

    with redirect_stdout(buffer):
        main.print_record(record)

    output = buffer.getvalue()
    assert "Фамилия: ИВАНОВ" in output
    assert "Данные: Илья, баскетбол" in output
    assert "V: 321" in output
    assert "h: 1" in output
    assert "Удален: False" in output


def test_load_demo_data_populates_hash_table():
    table = HashTable(size=20)
    buffer = StringIO()

    with redirect_stdout(buffer):
        main.load_demo_data(table)

    assert table.count == len(main.STUDENT_DATA)
    assert "=== ЗАГРУЗКА ДЕМОНСТРАЦИОННЫХ ДАННЫХ ===" in buffer.getvalue()


def test_add_student_creates_record(monkeypatch):
    table = HashTable(size=20)
    answers = iter(["Иванов", "Илья, баскетбол"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    buffer = StringIO()

    with redirect_stdout(buffer):
        main.add_student(table)

    assert table.read("Иванов").data == "Илья, баскетбол"
    assert "Успех: Запись добавлена" in buffer.getvalue()


def test_find_student_prints_record(monkeypatch):
    table = HashTable(size=20)
    table.create("Иванов", "Илья, баскетбол")
    monkeypatch.setattr("builtins.input", lambda _: "Иванов")
    buffer = StringIO()

    with redirect_stdout(buffer):
        main.find_student(table)

    output = buffer.getvalue()
    assert "=== ПОИСК СТУДЕНТА ===" in output
    assert "Фамилия: ИВАНОВ" in output


def test_update_student_updates_record(monkeypatch):
    table = HashTable(size=20)
    table.create("Иванов", "Илья, баскетбол")
    answers = iter(["Иванов", "Илья, программирование"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    buffer = StringIO()

    with redirect_stdout(buffer):
        main.update_student(table)

    output = buffer.getvalue()
    assert table.read("Иванов").data == "Илья, программирование"
    assert "Успех: Запись обновлена" in output
    assert "Фамилия: ИВАНОВ" in output


def test_delete_student_removes_record(monkeypatch):
    table = HashTable(size=20)
    table.create("Иванов", "Илья, баскетбол")
    monkeypatch.setattr("builtins.input", lambda _: "Иванов")
    buffer = StringIO()

    with redirect_stdout(buffer):
        main.delete_student(table)

    assert table.read("Иванов") is None
    assert "Успех: Запись удалена" in buffer.getvalue()


def test_print_menu_contains_all_commands():
    buffer = StringIO()

    with redirect_stdout(buffer):
        main.print_menu()

    output = buffer.getvalue()
    assert "1. Загрузить демонстрационные данные" in output
    assert "6. Показать таблицу" in output
    assert "0. Выход" in output


def test_handle_choice_loads_demo_data():
    table = HashTable(size=20)
    buffer = StringIO()

    with redirect_stdout(buffer):
        result = main.handle_choice("1", table)

    assert result is True
    assert table.count == len(main.STUDENT_DATA)


def test_handle_choice_prints_table():
    table = HashTable(size=20)
    buffer = StringIO()

    with redirect_stdout(buffer):
        result = main.handle_choice("6", table)

    assert result is True
    assert "ХЕШ-ТАБЛИЦА" in buffer.getvalue()


def test_handle_choice_exits_program():
    table = HashTable(size=20)
    buffer = StringIO()

    with redirect_stdout(buffer):
        result = main.handle_choice("0", table)

    assert result is False
    assert "Завершение программы" in buffer.getvalue()


def test_handle_choice_handles_unknown_command():
    table = HashTable(size=20)
    buffer = StringIO()

    with redirect_stdout(buffer):
        result = main.handle_choice("99", table)

    assert result is True
    assert "Неизвестная команда" in buffer.getvalue()


def test_run_cli_processes_commands_until_exit(monkeypatch):
    answers = iter(["1", "6", "0"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    buffer = StringIO()

    with redirect_stdout(buffer):
        main.run_cli()

    output = buffer.getvalue()
    assert "=== ЗАГРУЗКА ДЕМОНСТРАЦИОННЫХ ДАННЫХ ===" in output
    assert "ХЕШ-ТАБЛИЦА" in output
    assert "Завершение программы" in output


def test_main_calls_run_cli(monkeypatch):
    called = {"value": False}

    def fake_run_cli():
        called["value"] = True

    monkeypatch.setattr(main, "run_cli", fake_run_cli)

    main.main()

    assert called["value"] is True
