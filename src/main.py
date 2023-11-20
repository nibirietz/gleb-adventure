import random
import flet
import json

class MainWindow:
    def __init__(self) -> None:
        flet.app(target=self.main_loop)

    def main_loop(self, page: flet.Page):
        self.page = page
        self.page.title = "Приключение Глёбы"
        self.dialogue = Dialogue(self)
        self.question_text = flet.Text(self.dialogue.question)
        self.answers_button = flet.Row([flet.ElevatedButton(text=answer, on_click=self.dialogue.call_question) for answer in self.dialogue.answers])
        self.page.add(self.question_text, self.answers_button)

    def update_view(self, question, answers):
        self.page.remove(self.question_text, self.answers_button)
        self.question_text = flet.Text(question)
        self.answers_button = flet.Row([flet.ElevatedButton(text=answer, on_click=self.dialogue.call_question) for answer in answers])
        self.page.add(self.question_text, self.answers_button)


class Dialogue:
    def __init__(self, window: MainWindow):
        self.window = window
        with open("default.json", "r") as f:
            self.data = json.load(f)

        self.question = next(iter(self.data))
        self.answers = self.data[self.question]

    def call_question(self, arg):
        previuos_answer = arg.control.text
        if previuos_answer == "Выйти":
            self.window.page.window_destroy()
            return
        self.question = random.choice(self.data[previuos_answer])
        self.answers = self.data[self.question]
        self.window.update_view(self.question, self.answers)
            

def main():
    main_window = MainWindow()

if __name__ == "__main__":
    main()
