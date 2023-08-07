import openai
from os import environ

class GPT():
    def __init__(self) -> None:
        openai.api_key = environ.get('OPENAI_KEY')
        self.__messages = [{'role': 'user', 'content': 'ты голосовой ассистент по имени джарвис.'}, {'role': 'assistant', 'content': 'хорошо, давайте начнём наш диалог.'}]

    def request(self, task):
        try:
            self.__messages.append({'role': 'user', 'content': task})
            answer = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=self.__messages
            )
            result = answer.choices[0].message.content
            self.__messages.append({'role': 'assistant', 'content': result})
        except:
            result = 'похоже что-то пошло не так, мне не удалось выполнить запрос.'
        return result
