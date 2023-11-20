import flet
import json
import os
import icecream
from enum import Enum

class MainWindow:
    def __init__(self) -> None:
        pass

    def main_loop(self, page: flet.Page):
        self.page = page
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
        print()
        self.window.update_view(arg.control.text, self.data[arg.control.text])
            

def main():
    main_window = MainWindow()
    flet.app(target=main_window.main_loop)

if __name__ == "__main__":
    main()
