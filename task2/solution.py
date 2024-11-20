import requests
import json
import csv
import time


def fetch_animals(url, params):
    all_animals = []
    alphabet_counts = {}
    prev_letter = None

    while True:
        response = requests.get(url, params=params)
        data = response.json()

        for member in data["query"]["categorymembers"]:
            title = member["title"]

            # упрощенная логика, если это не животное а ссылка вида "Категория:Породы собак по алфавиту"
            if ":" in title:
                continue

            all_animals.append(title)

            first_letter = extract_first_letter(title, prev_letter)
            if first_letter:
                if first_letter not in alphabet_counts:
                    alphabet_counts[first_letter] = 0
                alphabet_counts[first_letter] += 1

            prev_letter = first_letter

        if "continue" in data:
            params["cmcontinue"] = data["continue"]["cmcontinue"]
        else:
            break

        time.sleep(0.5)

    return all_animals, alphabet_counts


def extract_first_letter(title, prev_letter):
    first_letter = title.split()[0][0].upper()

    # упрощенная логика парсинга, если не первое слово главное
    if prev_letter != first_letter:
        if prev_letter == title.split()[-1][0].upper():
            first_letter = prev_letter

    return first_letter


def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


def save_csv(filename, data):
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        for letter, count in data.items():
            writer.writerow([letter, count])


if __name__ == "__main__":
    URL = "https://ru.wikipedia.org/w/api.php"
    PARAMS = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": "Категория:Животные по алфавиту",
        "cmlimit": "max",
        "format": "json",
    }

    start_time = time.time()

    animals, counts = fetch_animals(URL, PARAMS)

    save_json("all_animals.json", animals)
    save_csv("beasts.csv", counts)

    print("Все данные сохранены:")
    print(" - Список животных: all_animals.json")
    print(" - Подсчет по буквам: beasts.csv")
    print(f"Время выполнения: {time.time() - start_time:.2f} секунд")
