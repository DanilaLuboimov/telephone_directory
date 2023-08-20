import os

from td_commands import add_random_records, show_directory, create_record, \
    search_record, edit_record
from utils import create_telephone_directory


def handler(c: str) -> None:
    """
    Обработчик введенной команды.

    :param c: Строка, вводимая пользователем.
    :return: None
    """
    command = ""
    arg = ""
    sep = True

    for i in c:
        if i == " " and sep:
            sep = False
        elif sep:
            command += i
        else:
            arg += i
    return shell(command, arg)


def shell(command: str, arg: str) -> None:
    """
    Вызов команд для работы с json-файлом.

    :param command: Вызываемая команда.
    :param arg: Аргументы для команды.
    :return: None
    """
    if command == "add_random_records":
        if arg:
            add_random_records(int(arg))
        else:
            add_random_records()
    elif command == "show_directory":
        if arg:
            show_directory(int(arg))
        else:
            show_directory()
    elif command == "exit":
        return True
    elif command == "create_record":
        create_record()
    elif command == "search_record":
        search_record()
    elif command == "edit_record":
        edit_record()
    elif command == "help":
        commands_help()
    else:
        print("Неизвестная команда!\n")


def commands_help() -> None:
    """
    Вывод подсказок по командам в консоли.

    :return: None
    """
    print(f"\nadd_random_records - Добавляет случайные записи "
          f"и принимает в качестве аргумента\nколичество необходимых записей."
          f"Изначальное количество равно 10\n"
          f"\nshow_directory - Позволяет просматривать содержимое справочника "
          f"и принимает в качестве аргумента\nколичество выводимых записей на"
          f"одной странице. Изначальное количество равно 5\n"
          f"\nsearch_record - Поиск записей по заданным параметрам\n"
          f"\ncreate_record - Команда для добавления новой записи в "
          f"справочник\n"
          f"\nedit_record - Команда для редактирования одной из записей "
          f"справочника\n"
          f"\nexit - Завершает работу программы\n")


print()

while True:
    if not os.path.exists("telephone directory.json"):
        create_telephone_directory()

    com = input("  Введите команду: ")

    if handler(com):
        break
