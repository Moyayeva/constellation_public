import json


# Функція для завантаження JSON-файлу
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Функція для форматування JSON-файлу
def json_formatting(context):
    fixed_context = []
    if "mapping" in context and type(context["mapping"]) is dict:
        for key, value in context["mapping"].items():
            create_msg = False
            thoughts = ""
            msg = ""
            if type(value) is dict:
                if "message" in value and type(value["message"]) is dict and  "author" in value["message"] and (value["message"]["author"]["role"] == "user" or value["message"]["author"]["role"] == "assistant" or value["message"]["author"]["name"] == "a8km123"):
                    message = {}
                    if  value["message"]["content"]["content_type"] == "text":
                        if "parts" in value["message"]["content"] and value["message"]["content"]["parts"][0] != "":
                            if value["message"]["author"]["role"] == "user" or value["message"]["author"]["role"] == "assistant":
                                msg = value["message"]["content"]["parts"][0]
                            else:
                                thoughts = value["message"]["content"]["parts"][0]
                            create_msg = True
                        elif "text" in value["message"]["content"] and value["message"]["content"]["text"] != "":
                            msg = value["message"]["content"]["text"]
                            create_msg = True

                    if value["message"]["content"]["content_type"] == "thoughts" and len(value["message"]["content"]["thoughts"]) != 0:
                        thoughts = value["message"]["content"]["thoughts"][0]["content"]
                        create_msg = True
                    if create_msg == True:
                        message["role"] = value["message"]["author"]["role"]
                        message["ts"] = value["message"]["create_time"]
                        if msg != "":
                            message["context"] = msg
                        if thoughts != "":
                            message["thoughts"] = thoughts
                        fixed_context.append(message)
            print(create_msg)

    return fixed_context

def move_thoughts_to_next_msg(fixed_context):
    context_iter = iter(fixed_context)
    context_with_thoughts = []
    for message in context_iter:
        if "thoughts" in message:
            thoughts = message["thoughts"]
            n = next(context_iter)["thoughts"] = thoughts
            print(n)
        context_with_thoughts.append(message)
    return context_with_thoughts


# Функція для збереження відформатованого JSON
def save_json(data, output_path):
    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

# Основна функція
def main(input_file, output_file):
    # Завантажуємо JSON
    data = load_json(input_file)
    # Сортуємо повідомлення
    sorted_data = json_formatting(data)
    # Зберігаємо відсортований JSON
    save_json(sorted_data, output_file)
    print(f"Messages sorted and saved to {output_file}")


# Виконання скрипту
if __name__ == "__main__":
    input_file = "context.json"  # Шлях до твого JSON-файлу
    output_file = "context.json"  # Шлях для збереження відсортованого файлу
    main(input_file, output_file)