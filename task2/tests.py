import pytest
import json
from unittest.mock import patch
from solution import extract_first_letter, fetch_animals, save_json, save_csv


# Тесты для extract_first_letter
@pytest.mark.parametrize(
    "title, prev_letter, expected",
    [
        ("Ёрш обыкновенный", None, "Ё"),
        ("Обыкновенный ёрш", "Ё", "Ё"),
        ("Ишхан (рыба)", "И", "И"),
    ],
)
def test_extract_first_letter(title, prev_letter, expected):
    assert extract_first_letter(title, prev_letter) == expected


# Тесты для fetch_animals
@patch("requests.get")
def test_fetch_animals(mock_get):
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
    assert animals == ["Ёрш обыкновенный", "Обыкновенный ёрш", "Ёрш Балона"]
    assert counts == {"Ё": 3}


# Тесты для save_json
def test_save_json(tmp_path):
    data = {"Ё": 3, "О": 1}
    file_path = tmp_path / "test.json"

    save_json(file_path, data)

    with open(file_path, encoding="utf-8") as f:
        saved_data = json.load(f)

    assert saved_data == data


# Тесты для save_csv
def test_save_csv(tmp_path):
    data = {"Ё": 3, "О": 1}
    file_path = tmp_path / "test.csv"

    save_csv(file_path, data)

    with open(file_path, encoding="utf-8") as f:
        lines = f.readlines()

    assert lines == ["Ё,3\n", "О,1\n"]
