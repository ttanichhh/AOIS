from hash_table import HashTable


STUDENT_DATA = [
    ("Соловей", "Илья, баскетбол"),
    ("Прокопчик", "Павел, шахматы"),
    ("Сташук", "Семен, программирование"),
    ("Попович", "Кирилл, музыка"),
    ("Панфило", "Никита, плавание"),
    ("Ровнейко", "Михаил, волейбол"),
    ("Носарь", "Федор, фотография"),
    ("Шитиков", "Олег, дизайн"),
    ("Трофимов", "Егор, робототехника"),
    ("Гаврилюк", "Вадим, настольный теннис"),
]


def print_result(success, message):
    if success:
        print("Успех:", message)
    else:
        print("Ошибка:", message)


def print_record(record):
    if record is None:
        print("Запись не найдена")
        return

    print("Фамилия:", record.key)
    print("Данные:", record.data)
    print("V:", record.value)
    print("h:", record.hash_address)
    print("Удален:", record.is_deleted)


def load_demo_data(hash_table):
    print("=== ЗАГРУЗКА ДЕМОНСТРАЦИОННЫХ ДАННЫХ ===")
    for surname, data in STUDENT_DATA:
        hash_table.print_hash_info(surname)
        success, message = hash_table.create(surname, data)
        print_result(success, message)
        print()


def add_student(hash_table):
    print("=== ДОБАВЛЕНИЕ СТУДЕНТА ===")
    surname = input("Введите фамилию: ")
    data = input("Введите данные (имя, увлечение): ")
    hash_table.print_hash_info(surname)
    success, message = hash_table.create(surname, data)
    print_result(success, message)


def find_student(hash_table):
    print("=== ПОИСК СТУДЕНТА ===")
    surname = input("Введите фамилию для поиска: ")
    record = hash_table.read(surname)
    print_record(record)


def update_student(hash_table):
    print("=== ОБНОВЛЕНИЕ СТУДЕНТА ===")
    surname = input("Введите фамилию для обновления: ")
    new_data = input("Введите новые данные: ")
    success, message = hash_table.update(surname, new_data)
    print_result(success, message)

    if success:
        print_record(hash_table.read(surname))


def delete_student(hash_table):
    print("=== УДАЛЕНИЕ СТУДЕНТА ===")
    surname = input("Введите фамилию для удаления: ")
    success, message = hash_table.delete(surname)
    print_result(success, message)

def print_menu():
    print("\n=== МЕНЮ ===")
    print("1. Загрузить демонстрационные данные")
    print("2. Добавить запись")
    print("3. Найти запись")
    print("4. Обновить запись")
    print("5. Удалить запись")
    print("6. Показать таблицу")
    print("0. Выход")


def handle_choice(choice, hash_table):
    if choice == "1":
        load_demo_data(hash_table)
    elif choice == "2":
        add_student(hash_table)
    elif choice == "3":
        find_student(hash_table)
    elif choice == "4":
        update_student(hash_table)
    elif choice == "5":
        delete_student(hash_table)
    elif choice == "6":
        hash_table.print_table()
    elif choice == "0":
        print("Завершение программы")
        return False
    else:
        print("Неизвестная команда. Повторите ввод.")

    return True


def run_cli():
    hash_table = HashTable()


    is_running = True
    while is_running:
        print_menu()
        choice = input("Выберите пункт меню: ").strip()
        is_running = handle_choice(choice, hash_table)


def main():
    run_cli()


if __name__ == "__main__":
    main()
