import random
import flet
import json
from urllib.request import urlretrieve


JSON_FILE = "script.json"
try:
    urlretrieve("https://raw.githubusercontent.com/nibirietz/gleb-adventure/main/script.json", "script.json")
except FileNotFoundError as e:
    print(e)

class MainWindow:
    def __init__(self):
        flet.app(target=self.main_loop)

    def main_loop(self, page: flet.Page):
        self.page = page
        self.page.title = "Приключение Глёбы"
        self.dialogue = Script(self)
        self.question_text = flet.Text(self.dialogue.question)
        self.answers_button = flet.Row([flet.ElevatedButton(text=answer, on_click=self.dialogue.call_question) for answer in self.dialogue.answers])
        self.page.add(self.question_text, self.answers_button)

    def update_view(self, question, answers):
        """
        Обновляет вид, меняя вопрос и ответы на новые.
        """
        self.page.remove(self.question_text, self.answers_button)
        self.question_text = flet.Text(question)
        self.answers_button = flet.Row([flet.ElevatedButton(text=answer, on_click=self.dialogue.call_question) for answer in answers])
        self.page.add(self.question_text, self.answers_button)


class Script:
    def __init__(self, window: MainWindow):
        """
        Инициализирует сценарий с начального вопроса, в качестве параметра получает окно(пока что главное).
        """
        self.window = window
        with open(JSON_FILE, "r", encoding="utf") as f:
            self.data = json.load(f)

        self.question = next(iter(self.data))
        self.answers = self.data[self.question]

    def call_question(self, arg):
        """
        Получает control. Достаёт со скрипта вопрос и его ответы.
        """
        previuos_answer = arg.control.text
        if previuos_answer == "Выйти":
            self.window.page.window_destroy()
            return
        if previuos_answer not in self.data:
            self.window.update_view("Дальше бога нет.", ["Выйти"])
        else:
            self.question = random.choice(self.data[previuos_answer])
            try:
                self.answers = self.data[self.question]
                self.window.update_view(self.question, self.answers)
            except Exception:
                self.window.update_view(self.question, ["Выйти"])
            

def main():
    main_window = MainWindow()

if __name__ == "__main__":
    main()
