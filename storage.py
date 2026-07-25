import json

def save(work_time):
    with open("config.json", "w", encoding="utf-8") as file:
        json.dump(work_time, file, indent=4, ensure_ascii=False)

def load():
    try:
        with open('config.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        work_time = data
        return work_time
    except FileNotFoundError:
        return {}