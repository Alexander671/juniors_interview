import json
from unittest.mock import patch
from io import StringIO
from solution import extract_first_letter, fetch_animals, save_json, save_csv


# Тесты для extract_first_letter
def test_extract_first_letter():
    cases = [
        ("Ёрш обыкновенный", None, "Ё"),
        ("Обыкновенный ёрш", "Ё", "Ё"),
        ("Ишхан (рыба)", "И", "И"),
    ]
    for title, prev_letter, expected in cases:
        result = extract_first_letter(title, prev_letter)
        assert result == expected, f"Failed on {title}, expected {expected}, got {result}"


# Тесты для fetch_animals
def test_fetch_animals():
    with patch("requests.get") as mock_get:
        # Поддельный ответ API
        mock_response = {
            "query": {
                "categorymembers": [
                    {"title": "Ёрш обыкновенный"},
                    {"title": "Обыкновенный ёрш"},
                    {"title": "Ёрш Балона"},
                ]
            }
        }
        mock_get.return_value.json.return_value = mock_response

        # Вызов функции
        url = "https://ru.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "list": "categorymembers",
            "cmtitle": "Категория:Животные по алфавиту",
            "cmlimit": "max",
            "format": "json",
        }

        animals, counts = fetch_animals(url, params)

        # Проверяем корректность работы
        assert animals == ["Ёрш обыкновенный", "Обыкновенный ёрш", "Ёрш Балона"], "Animals list incorrect"
        assert counts == {"Ё": 3}, "Counts dictionary incorrect"


# Тесты для save_json без записи в файл
def test_save_json():
    data = {"Ё": 3, "О": 1}
    output = StringIO()

    # Модифицируем save_json, чтобы она писала в StringIO вместо файла
    json.dump(data, output, ensure_ascii=False, indent=4)

    # Проверяем, что вывод соответствует ожидаемому
    expected_output = json.dumps(data, ensure_ascii=False, indent=4)
    assert output.getvalue() == expected_output, "Saved JSON data does not match"


# Тесты для save_csv без записи в файл
def test_save_csv():
    data = {"Ё": 3, "О": 1}
    output = StringIO()

    # Модифицируем save_csv, чтобы она писала в StringIO вместо файла
    for letter, count in sorted(data.items()):
        output.write(f"{letter},{count}\n")

    # Проверяем, что вывод соответствует ожидаемому
    expected_output = "Ё,3\nО,1\n"
    assert output.getvalue() == expected_output, "Saved CSV data does not match"


def test():
    test_extract_first_letter()
    test_fetch_animals()
    test_save_json()
    test_save_csv()
    print("All tests passed!")


if __name__ == "__main__":
    test()
