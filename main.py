import flet
import json
from urllib.request import urlretrieve
import sys


JSON_FILE = "script.json"
if "test" not in sys.argv:
    try:
        urlretrieve("https://raw.githubusercontent.com/nibirietz/gleb-adventure/main/script.json", "script.json")
    except FileNotFoundError as e:
        print(e)

class MainWindow:
    def __init__(self):
        flet.app(target=self.main_loop)

    def main_loop(self, page: flet.Page):
        self.page = page
        self.page.title = "Когда плачут Глёбы"
        self.dialogue = Script(self)
        self.question_text = flet.Text(self.dialogue.question)
        self.answers_button = flet.Row([flet.ElevatedButton(text=answer, on_click=self.dialogue.call_question) for answer in self.dialogue.answers])
        self.page.add(flet.Container(image_src="yurta.png", image_fit=flet.ImageFit.COVER, expand=True), 
        self.question_text, self.answers_button)

    def update_view(self, question, answers):
        self.page.remove(self.question_text, self.answers_button)
        self.question_text = flet.Text(question)
        self.answers_button = flet.Row([flet.ElevatedButton(text=answer, on_click=self.dialogue.call_question) for answer in answers])
        self.page.add(self.question_text, self.answers_button)

        

class Script:
    def __init__(self, window: MainWindow):
        self.window = window
        with open(JSON_FILE, "r", encoding="utf") as f:
            self.data = json.load(f)

        self.first_question = next(iter(self.data))
        self.question = self.first_question
        self.answers = self.data[self.question]

    def call_question(self, arg):
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
            self.window.update_view("Дальше бога нет.", ["Да и хрен с ним", "Начать заново"])
            
            

def main():
    main_window = MainWindow()

if __name__ == "__main__":
    main()
