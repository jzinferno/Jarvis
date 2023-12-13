from openai import  OpenAI
from os import environ

class GPT():
    def __init__(self) -> None:
        self.client = OpenAI(api_key=environ.get("OPENAI_KEY"))
        self.__messages = [{'role': 'user', 'content': 'ты голосовой ассистент по имени джарвис.'}, {'role': 'assistant', 'content': 'хорошо, давайте начнём наш диалог.'}]

    def request(self, task):
        if True:
            self.__messages.append({'role': 'user', 'content': task})
            completion = self.client.chat.completions.create(
                messages=self.__messages,
                model='gpt-3.5-turbo'
            )
            result = completion.choices[0].message.content
            self.__messages.append({'role': 'assistant', 'content': result})
        else:
            result = 'похоже что-то пошло не так, мне не удалось выполнить запрос.'
        return result
