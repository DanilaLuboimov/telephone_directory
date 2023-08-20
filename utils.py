import json
import random
import re

CITY_CODE: tuple = ("385", "495", "499", "381", "384",
                    "812", "817", "820", "831", "815")


def gen_phone(optional: str = "w") -> str:
    """
    Генерирует телефонные номера для рабочего и личного телефона.

    :param optional: Определяет какой тип номера будет сгенерирован.
    :return: str
    """
    second: str = str(random.randint(1, 999)).zfill(3)
    last: str = str(random.randint(1, 9999)).zfill(4)

    if optional == "w":
        city_code = random.choice(CITY_CODE)
        return f"{city_code}{second}{last}"

    first: str = str(random.randint(100, 999))
    return f"8{first}{second}{last}"


def create_telephone_directory() -> None:
    """
    Создает json-файл для хранения записей в справочнике.

    :return: None
    """
    with open("telephone directory.json", "w", encoding="utf-8") as file:
        data: list = []
        json.dump(data, file, indent=4, ensure_ascii=False)


def response_json(data: list, limit: int, page: int, total_results: int,
                  total_page: int) -> str:
    """
    Возвращает фрагмент json-файла.

    :param data: Массив данных.
    :param limit: Максимум записей во фрагменте.
    :param page: Номер фрагмента массива данных из файла.
    :param total_results: Всего записей в файле.
    :param total_page: Максимум фрагментов в файле.
    :return: str
    """
    start_rec: int = (page - 1) * limit
    end_rec: int = page * limit if total_page >= page else total_results
    res: str = "\n".join(
        [', '.join(rec.values()) for rec in data[start_rec:end_rec]]
    )
    return res


def check_regex_phone(phone: str) -> bool:
    """
    Проверка валидности введенного телефона.

    :param phone: Телефон, например +7(931)1234567 или 83331234562
    :return: bool
    """
    return re.search(r"^(\+7|8)[(]?\d{3}[)]?\d{7}$", phone)


def serializer_search_param(param: str) -> [str | None]:
    """
    Преобразует ввод пользователя под параметры json-файла
    и проверяет валидность ввода.

    :param param: Параметр для поиска записи.
    :return: [str | None]
    """
    if param == "id":
        return param
    elif param == "фамилия":
        return "last_name"
    elif param == "имя":
        return "first_name"
    elif param == "отчество":
        return "middle_name"
    elif param == "название организации":
        return "company"
    elif param == "телефон рабочий":
        return "work phone number"
    elif param == "телефон личный":
        return "personal phone number"
    else:
        return None


def serializer_param_directory(param: str) -> str:
    """
    Преобразует параметры json-файла для пользователя.

    :param param: Параметр записи.
    :return: str
    """
    if param == "last_name":
        return "фамилия"
    elif param == "first_name":
        return "имя"
    elif param == "middle_name":
        return "отчество"
    elif param == "company":
        return "название организации"
    elif param == "work phone number":
        return "телефон рабочий"
    elif param == "personal phone number":
        return "телефон личный"
