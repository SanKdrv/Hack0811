import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer
from threading import Thread
import sys
import re


class AIRequest:
    def __init__(self, model_path):
        # print("================>   " + model_path)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        # print(f"Using device: {self.device}")

        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype="auto",
            device_map="auto",
            trust_remote_code=True,
            low_cpu_mem_usage=True
        )
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)

    def analyze(self, prompt):
        messages = [
            {"role": "system",
             "content": "Ты - диспетчер. Ты делаешь только то, о чем тебя просят."},
            {"role": "user", "content": prompt}
        ]
        text = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)

        generated_ids = self.model.generate(
            **model_inputs,
            max_new_tokens=512,
            do_sample=False,
            temperature=0.0
        )
        generated_ids = generated_ids[:, model_inputs.input_ids.shape[-1]:]

        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        # print(response)
        # Извлекаем текст между маркерами
        start_marker = '```json'
        end_marker = '```'

        # Находим начало и конец содержимого
        start_index = response.find(start_marker) + len(start_marker)
        end_index = response.find(end_marker, start_index)

        # Если хотя бы один из маркеров не найден, возвращаем оригинальный ответ
        if start_index == -1 or end_index == -1:
            return response

        # print(start_index, end_index)
        response = response[start_index:end_index].strip()

        # Извлекаем текст между маркерами и убираем лишние пробелы или символы новой строки
        return response


def main():
    # Пример использования:
    ai = AIRequest(".")
    with open("promts/request_test.txt", "r", encoding="utf-8") as file:
        request = file.read().strip()
    result = ai.analyze(request)
    print(result)  # Раскомментируйте, если хотите вывести результат еще раз

    # Чтение запроса из файла
    with open("promts/request1.txt", "r", encoding="utf-8") as file:
        request = file.read().strip()
    # result = ai.analyze(request)
    # print(result)  # Раскомментируйте, если хотите вывести результат еще раз

    with open("promts/request2.txt", "r", encoding="utf-8") as file:
        request = file.read().strip()
    # result = ai.analyze(request)
    # print(result)  # Раскомментируйте, если хотите вывести результат еще раз

    with open("promts/request3.txt", "r", encoding="utf-8") as file:
        request = file.read().strip()
    # result = ai.analyze(request)
    # print(result)  # Раскомментируйте, если хотите вывести результат еще раз

    with open("promts/request4.txt", "r", encoding="utf-8") as file:
        request = file.read().strip()
    # result = ai.analyze(request)
    # print(result)  # Раскомментируйте, если хотите вывести результат еще раз


if __name__ == "__main__":
    main()
