import flet
import csv
from urllib.request import urlretrieve


class MainWindow:
    def __init__(self):
        self.picture = flet.Container(
            image_src="data/images/yurta.png",
            image_fit=flet.ImageFit.COVER,
            expand=True,
        )
        flet.app(target=self.main_loop)

    def main_loop(self, page: flet.Page):
        self.page = page
        self.page.title = "Когда плачут Глёбы"
        self.dialogue = Script(self)
        self.question_text = flet.Text(self.dialogue.first_question)
        self.answers_button = flet.Row(
            [
                flet.ElevatedButton(text=answer, on_click=self.dialogue.call_question)
                for answer in self.dialogue.answers
            ]
        )

        self.page.add(self.question_text, self.answers_button, self.picture)

    def update_view(self, question: str, answers: list[str], picture=None):
        self.page.remove(self.question_text, self.answers_button, self.picture)
        if picture != None:
            self.picture = flet.Container(
                image_src=picture, image_fit=flet.ImageFit.COVER, expand=True
            )
        self.question_text = flet.Text(question)
        self.answers_button = flet.Row(
            [
                flet.ElevatedButton(text=answer, on_click=self.dialogue.call_question)
                for answer in answers
            ]
        )
        self.page.add(self.question_text, self.answers_button, self.picture)


class Script:
    def __init__(self, window: MainWindow):
        self.window = window
        with open("data/script.csv", encoding="utf-8") as csvfile:
            self.data = list(csv.DictReader(csvfile))

        self.first_question = self.data[0]["Вопрос"]
        self.desciption = self.data[0]["Описание"]
        self.answers = self.parse_question(self.data[0]["Ответы"])

    def parse_question(self, line: str) -> list[str]:
        if line == "@":
            return ["Выйти", "Начать заново"]
        return line.split("|")

    def call_question(self, arg):
        previous_answer = arg.control.text
        print(self.desciption, self.answers, previous_answer)
        if previous_answer == "Выйти":
            self.window.page.window_destroy()
            return
        if previous_answer == "Начать заново":
            self.desciption = self.first_question
            self.answers = self.parse_question(self.data[0]["Ответы"])
            self.window.update_view(self.desciption, self.answers)
            return

        for row in self.data:
            print(row)
            if row["Вопрос"] == previous_answer:
                self.desciption = row["Описание"]
                self.answers = self.parse_question(row["Ответы"])
                self.window.update_view(
                    self.desciption, self.answers, self.get_image(row["Картинка"])
                )
                return
        else:
            self.window.update_view("Дальше бога нет.", ["Выйти", "Начать заново"])

    def get_image(self, image: str) -> str | None:
        if image == "@":
            return None
        return "data/images/" + image


def main():
    main_window = MainWindow()


if __name__ == "__main__":
    main()
