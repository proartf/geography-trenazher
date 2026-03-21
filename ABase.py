import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import time
import subprocess
import os
import winsound

class Windows11FinalFix:
    def __init__(self, root):
        self.root = root
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg="#0078d7")
        self.root.config(cursor="none") 

        # --- BSOD ИНТЕРФЕЙС ---
        self.main_frame = tk.Frame(self.root, bg="#0078d7")
        self.main_frame.place(relx=0.1, rely=0.2, anchor="nw")

        tk.Label(self.main_frame, text=":(", font=("Segoe UI", 120), bg="#0078d7", fg="white").pack(anchor="w")
        tk.Label(self.main_frame, text="Your PC ran into a problem and needs to restart...", 
                 font=("Segoe UI", 22), bg="#0078d7", fg="white", justify="left").pack(anchor="w", pady=20)

        self.progress_val = 0
        self.perc_lbl = tk.Label(self.main_frame, text="0% complete", font=("Segoe UI", 24), bg="#0078d7", fg="white")
        self.perc_lbl.pack(anchor="w", pady=10)

        # QR-код
        self.qr_canvas = tk.Canvas(self.main_frame, width=100, height=100, bg="white", highlightthickness=0)
        self.qr_canvas.pack(anchor="w", pady=20)
        self.generate_qr()

        self.update_progress()

    def generate_qr(self):
        for _ in range(300):
            x, y = random.randint(0, 100), random.randint(0, 100)
            self.qr_canvas.create_rectangle(x, y, x+5, y+5, fill="black", outline="")

    def update_progress(self):
        if self.progress_val < 100:
            self.progress_val += random.randint(10, 25)
            if self.progress_val > 100: self.progress_val = 100
            self.perc_lbl.config(text=f"{self.progress_val}% complete")
            self.root.after(random.randint(400, 1000), self.update_progress)
        else:
            self.root.after(1000, self.fade_out)

    def fade_out(self):
        # Плавное исчезновение
        alpha = self.root.attributes("-alpha")
        if alpha > 0.1:
            self.root.attributes("-alpha", alpha - 0.1)
            self.root.after(50, self.fade_out)
        else:
            self.show_vbs_and_gnome()

    def show_vbs_and_gnome(self):
        # 1. Системное окно
        vbs = "msg.vbs"
        with open(vbs, "w", encoding="cp1251") as f:
            f.write('MsgBox "Ну ты и дурак, вот нефиг было качать что попало с рандомных сайтов!", 48, "System Security"')
        
        subprocess.run(["wscript.exe", vbs])
        
        # 2. Показываем гриба
        self.root.attributes("-alpha", 1.0)
        self.root.configure(bg="black")
        self.main_frame.destroy()

        # Путь к картинке
        img_path = "prostofilya.jfif"
        
        if os.path.exists(img_path):
            try:
                img = Image.open(img_path)
                sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
                img = img.resize((sw, sh), Image.Resampling.LANCZOS)
                self.photo = ImageTk.PhotoImage(img)
                tk.Label(self.root, image=self.photo, bg="black").place(relx=0.5, rely=0.5, anchor="center")
                winsound.MessageBeep(winsound.MB_ICONHAND)
            except Exception as e:
                tk.Label(self.root, text=f"Ошибка картинки: {e}", fg="white", bg="black").pack()
        else:
            tk.Label(self.root, text="ГДЕ ГРИБ? Положи prostofilya.jfif в папку!", 
                     font=("Arial", 30), fg="red", bg="black").place(relx=0.5, rely=0.5, anchor="center")

        if os.path.exists(vbs): os.remove(vbs)
        self.root.after(5000, self.root.destroy)

if __name__ == "__main__":
    root = tk.Tk()
    root.bind("<Escape>", lambda e: root.destroy())
    app = Windows11FinalFix(root)
    root.mainloop()
