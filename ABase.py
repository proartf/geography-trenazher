import customtkinter as ctk
from PIL import Image
import random
import io
import requests
from Flags import FLAGS

ctk.set_appearance_mode("dark")


class FlagQuiz(ctk.CTk):
    score = 0

    def __init__(self):
        super().__init__()

        self.title("AGeography - Тренажер флагов")
        self.geometry("500x450")
        self.data = FLAGS
        self.current_question = {}
        self.flag_label = ctk.CTkLabel(self, text="Загрузка...")
        self.flag_label.pack(pady=20)
        self.buttons = []

        for i in range(3):
            btn = ctk.CTkButton(
                self, text=f"Вариант {i+1}", command=lambda b=i: self.check_answer(b)
            )
            btn.pack(pady=5)
            self.buttons.append(btn)

        self.score_counter = ctk.CTkLabel(self, text="Игра еще не начата...")
        self.score_counter.pack()

        self.next_question()

    def next_question(self):
        self.current_question = random.choice(self.data)
        img_source = self.current_question["image"]

        try:

            if img_source.startswith("http"):
                response = requests.get(img_source)
                raw_data = io.BytesIO(response.content)
                img = Image.open(raw_data)
            else:
                img = Image.open(img_source)

            my_image = ctk.CTkImage(light_image=img, size=(250, 150))
            self.flag_label.configure(image=my_image, text="")
            self.flag_label.image = my_image

        except Exception as e:
            self.flag_label.configure(image=None, text="Не удалось загрузить флаг")

        correct_answer = self.current_question["name"]
        others = [d["name"] for d in self.data if d["name"] != correct_answer]
        options = random.sample(others, 2) + [correct_answer]
        random.shuffle(options)

        for i in range(3):
            self.buttons[i].configure(text=options[i], fg_color="#1f538d")

        self.score_counter.configure(text=self.score_label_text())

    def check_answer(self, btn_index):
        selected = self.buttons[btn_index].cget("text")
        if selected == self.current_question["name"]:
            self.buttons[btn_index].configure(fg_color="green")
            self.score += 1
            self.after(1000, self.next_question)
        else:
            self.score = 0
            self.score_counter.configure(text=self.score_label_text())
            self.buttons[btn_index].configure(fg_color="red")

    def get_payer_rank(self) -> str:
        if self.score < 5:
            return "Новичок"
        if self.score < 10:
            return "Начинающий"
        if self.score < 15:
            return "Энтузиаст"
        if self.score < 20:
            return "Знаток"
        return "Легенда"

    def score_label_text(self) -> str:
        return (
            "Правильных ответов подряд: "
            + str(self.score)
            + "\n"
            + "Твой ранг: "
            + self.get_payer_rank()
        )


if __name__ == "__main__":
    app = FlagQuiz()
    app.mainloop()
