import json
import random

from math import ceil as round_up

from utils import gen_phone, response_json, check_regex_phone, \
    serializer_search_param, serializer_param_directory

FIRST_NAMES_M: tuple = ("Евгений", "Павел", "Егор", "Иван", "Игорь", "Алексей",
                        "Рафик", "Кирилл", "Арсений")
FIRST_NAMES_F: tuple = ("Оксана", "Зоя", "Алла", "Алина", "Ира", "Кристина",
                        "Ксения", "Анна")
MIDDLE_NAMES: tuple = ("Абрамович", "Григорьевич", "Максимович", "Матвеевич",
                       "Наумович", "Олегович", "Павлович", "Иванович")
LAST_NAMES: tuple = ("Смирнов", "Соколов", "Лебедев", "Крылов", "Быков",
                     "Ефремов", "Одинцов", "Якушев", "Доронин", "Русаков",
                     "Тимофеев", "Туров", "Гришин", "Молчанов", "Наумов",
                     "Давыдов", "Королёв")
COMPANIES: tuple = (
    "Авито", "2ГИС", "3D Realms", "Автолайн", "АвтоВАЗ", "Аквариус", "Белкард",
    "Биотэк", "ВирусБлокАда", "Витебские ковры", "Газпром", "Гомелькабель",
    "Данон Россия", "Додо Пицца", "Дримкар", "Жолнаи", "Квадра",
    "Красносельский Ювелирпром", "Л1", "Криогенмаш", "Кузница на Рыбальском",
    "Леккер", "М.Видео", "Мираторг", "Новая Афина", "Петон", "Спецлит")


def add_random_records(count: int = 10) -> None:
    """
    Добавляет случайные записи.

    :param count: Количество добавляемых записей.
    :return: None
    """
    if str(count).isalpha() or count < 0:
        count: int = 10

    with open("telephone directory.txt", "r", encoding="utf-8") as file:
        data: list[dict] = json.load(file)

        for _ in range(count):
            sex: bool = random.randint(0, 1)
            middle_name: str = random.choice(MIDDLE_NAMES)
            last_name: str = random.choice(LAST_NAMES)
            company: str = random.choice(COMPANIES)

            if sex == 1:
                first_name: str = random.choice(FIRST_NAMES_M)
            else:
                first_name: str = random.choice(FIRST_NAMES_F)
                middle_name: str = middle_name[:-2:] + "на"
                last_name: str = last_name + "а"

            record: dict = {
                "id": str(len(data)),
                "last_name": last_name,
                "first_name": first_name,
                "middle_name": middle_name,
                "company": company,
                "work phone number": gen_phone(),
                "personal phone number": gen_phone("p"),
            }

            data.append(record)

        with open("telephone directory.txt", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print(f"Количество добавленных записей: {count}\n")


def show_directory(limit: int = 5) -> None:
    """
    Просмотреть содержимое справочника.

    :param limit: Максимум выводимых записей на странице.
    :return: None
    """
    with open("telephone directory.txt", "r", encoding="utf-8") as file:
        data: list[dict] = json.load(file)
        total_results = len(data)
        total_page: int = round_up(total_results / limit)
        page: int = 1

    print(f" Первая страница из {total_page}", end="\n\n")
    print(response_json(data, limit, page, total_page, total_results))

    while True:
        com = input("  Выберите куда двигаться (previous/next). "
                    "Или cancel для выхода: ")

        if com == "previous":
            print("\nПредыдущая страница.", end=" ")
            page -= 1
        elif com == "next":
            print("\nСледующая страница.", end=" ")
            page += 1
        elif com == "cancel":
            print("\nВыход из каталога")
            break
        else:
            print("\nНедоступная команда")
            continue

        if page < 1:
            page: int = 1
        elif page > total_page:
            page: int = total_page

        res: str = response_json(data, limit, page, total_page, total_results)

        print(f"Страница {page}/{total_page}", end="\n\n")
        print(res, end="\n\n")


def create_record() -> str:
    """
    Добавление новой записи в справочник.

    :return: str
    """
    print("\n Создание новой записи в справочнике\n")
    last_name: str = input("  Введите фамилию: ")
    first_name: str = input("  Введите имя: ")
    middle_name: str = input("  Введите отчество: ")
    company: str = input("  Введите название организации: ")

    while True:
        work_phone: str = input("  Введите рабочий телефон: ")

        if len(work_phone) != 10 and work_phone != "-":
            print(' Вы ввели неверный номер. Если вы не знаете'
                  ' номер введите "-"')
            continue

        break

    while True:
        personal_phone: str = input("  Введите личный телефон: ")

        if personal_phone == "-" or check_regex_phone(personal_phone):
            break

        print(' Вы ввели неверный номер. '
              'Пример номера: "+7(931)1234567" "83331234562"\n'
              ' Если вы не знаете номер введите "-"')

    with open("telephone directory.txt", "r", encoding="utf-8") as file:
        data: list[dict] = json.load(file)

        record: dict = {
            "id": str(len(data)),
            "last_name": last_name,
            "first_name": first_name,
            "middle_name": middle_name,
            "company": company,
            "work phone number": work_phone,
            "personal phone number": personal_phone,
        }

        data.append(record)

        with open("telephone directory.txt", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    print("\n Запись успешно добавлена!\n"
          f" Полученная запись: {', '.join(record.values())}", end="\n\n")


def search_record() -> None:
    """
    Поиск записи по фильтрам.

    :return: None
    """
    flag: bool = False

    print(" Критерии для поиска: id, фамилия, имя, отчество, "
          "название организации, телефон рабочий, телефон личный\n"
          "Для отмены введите cancel")

    filters: set = set()

    while True:
        param: str = input("  Введите один из параметров или stop: ")

        if param.lower() == "cancel":
            flag: bool = True
            break
        elif param.lower() == "stop":
            break
        else:
            new_param: [str | None] = serializer_search_param(param.lower())

        if new_param:
            filters.add((new_param, param))
        else:
            print(f"Неверный параметр: {param}")

    if flag:
        return

    request_params: dict = {}

    for i in filters:
        request_params[i[0]] = input(f"  Введите содержимое поля {i[1]}: ")

    with open("telephone directory.txt", "r", encoding="utf-8") as file:
        data: list[dict] = json.load(file)

        response: list = []

        for rec in data:
            check_list: dict = {i: False for i in request_params.keys()}

            for k, v in rec.items():
                if k in request_params.keys():
                    if request_params[k].lower() in v.lower():
                        check_list[k]: bool = True

            if all(check_list.values()):
                response.append(", ".join(rec.values()))

    print()

    if len(response) == 0:
        print("К сожалению не удалось найти записи по вашим параметрам",
              end="\n\n")
    else:
        print("\n".join(response), end="\n\n")


def edit_record() -> None:
    """
    Редактирование записи из json-файла.

    :return: None
    """
    with open("telephone directory.txt", "r", encoding="utf-8") as file:
        data: list[dict] = json.load(file)

        print("\n Если вы не помните или не знаете id записи - введите search "
              "или cancel для отмены редактирования")

        while True:
            id_rec: str = input("  Введите id записи для редактирования: ")

            if id_rec == "search":
                search_record()
                continue

            break

        flag: bool = True

        for rec in data:
            if rec["id"] == id_rec:
                flag: bool = False
                break

        if flag:
            print(" К сожалению записи с таким id не существует")
            return

        old_rec: dict = rec.copy()

        print(f"\n Найденная запись: {', '.join(rec.values())}", end="\n\n")

        for field, value in rec.items():
            if field == "id":
                continue

            while True:
                val: str = input(
                    f'  Поле: {serializer_param_directory(field)}\n'
                    f'  Текущее значение: {value}\n'
                    f'  Введите новое значение или оставьте поле пустым: '
                )
                print()

                if val == "":
                    val: str = value

                if field == "work phone number" and len(val) != 10 \
                        and val != "-":

                    print('\n Вы ввели неверный номер. Если вы не знаете'
                          ' номер введите "-"')
                    continue

                if field == "personal phone number":
                    if val == "-" or check_regex_phone(val):
                        break

                    print('\n Вы ввели неверный номер. '
                          'Пример номера: "+7(931)1234567" "83331234562"\n'
                          ' Если вы не знаете номер введите "-"')
                    continue

                break

            rec[field] = val

        print(f"\n Старая запись: {', '.join(old_rec.values())}")
        print(f" Новая запись: {', '.join(rec.values())}\n")

        with open("telephone directory.txt", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
