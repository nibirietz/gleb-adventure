import flet
import json
from urllib.request import urlretrieve
import sys


class MainWindow:
    def __init__(self):
        flet.app(target=self.main_loop)

    def main_loop(self, page: flet.Page):
        self.page = page
        self.page.title = "Когда плачут Глёбы"
        self.dialogue = Script(self)
        self.question_text = flet.Text(self.dialogue.question)
        self.answers_button = flet.Row(
            [
                flet.ElevatedButton(text=answer, on_click=self.dialogue.call_question)
                for answer in self.dialogue.answers
            ]
        )
        self.page.add(self.question_text, self.answers_button)

    def update_view(self, question: str, answers: list[str]):
        self.page.remove(self.question_text, self.answers_button)
        self.question_text = flet.Text(question)
        self.answers_button = flet.Row(
            [
                flet.ElevatedButton(text=answer, on_click=self.dialogue.call_question)
                for answer in answers
            ]
        )
        self.page.add(self.question_text, self.answers_button)


class Script:
    def __init__(self, window: MainWindow):
        self.window = window
        with open("data/script.json", "r", encoding="utf") as file:
            self.data = json.load(file)

        self.first_question = next(iter(self.data))
        self.question = self.first_question
        self.answers = self.data[self.question]

    def download_files(self):
        if "test" not in sys.argv:
            with open("data/urls.txt", "r") as file:
                try:
                    urlretrieve(file.readline())
                except FileExistsError as e:
                    print(e)

    def call_question(self, arg):
        """
        self.data[0] - описание
        self.data[1:] - ответы
        """
        previous_answer = arg.control.text
        if previous_answer == "Да и хрен с ним":
            self.window.page.window_destroy()
        if previous_answer == "Начать заново":
            self.question = self.first_question
            self.answers = self.data[self.question]
            self.window.update_view(self.question, self.answers)
            return
        try:
            self.question = self.data[previous_answer][0]
            self.answers = self.data[previous_answer][1:]
            self.window.update_view(self.question, self.answers)
        except Exception:
            self.window.update_view(
                "Дальше бога нет.", ["Да и хрен с ним", "Начать заново"]
            )


def main():
    main_window = MainWindow()


if __name__ == "__main__":
    main()
