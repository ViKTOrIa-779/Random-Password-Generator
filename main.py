import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
from datetime import datetime

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.root.geometry("500x400")

        # Элементы интерфейса
        self.create_widgets()
        self.load_history()

    def create_widgets(self):
        # Ползунок длины пароля (6–32 символа)
        ttk.Label(self.root, text="Длина пароля (6–32):").grid(row=0, column=0, padx=10, pady=5)
        self.length_scale = ttk.Scale(self.root, from_=6, to=32, orient='horizontal', command=self.update_length)
        self.length_scale.set(12)
        self.length_scale.grid(row=0, column=1, padx=10, pady=5, columnspan=3)

        # Чекбоксы для выбора символов
        self.use_digits = tk.BooleanVar(value=True)
        ttk.Checkbutton(self.root, text="Цифры (0–9)", variable=self.use_digits).grid(row=1, column=0, padx=10, pady=5)

        self.use_letters = tk.BooleanVar(value=True)
        ttk.Checkbutton(self.root, text="Буквы (a–z, A–Z)", variable=self.use_letters).grid(row=1, column=1, padx=10, pady=5)

        self.use_special = tk.BooleanVar(value=True)
        ttk.Checkbutton(self.root, text="Спецсимволы", variable=self.use_special).grid(row=1, column=2, padx=10, pady=5)

        # Кнопка генерации
        self.generate_btn = ttk.Button(self.root, text="Сгенерировать пароль", command=self.generate_password)
        self.generate_btn.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        # Поле для вывода пароля
        self.password_var = tk.StringVar()
        ttk.Label(self.root, text="Сгенерированный пароль:").grid(row=3, column=0, padx=10, pady=5)
        ttk.Entry(self.root, textvariable=self.password_var, font=("Arial", 12), width=30).grid(row=3, column=1, columnspan=3, padx=10, pady=5)

        # Таблица истории
        ttk.Label(self.root, text="История паролей:").grid(row=4, column=0, padx=10, pady=5)
        self.history_tree = ttk.Treeview(self.root, columns=("password", "length", "timestamp"), show="headings", height=10)
        self.history_tree.heading("password", text="Пароль")
        self.history_tree.heading("length", text="Длина")
        self.history_tree.heading("timestamp", text="Время создания")
        self.history_tree.grid(row=5, column=0, columnspan=4, padx=10, pady=5)

    def update_length(self, value):
        self.password_length = int(float(value))

    def generate_password(self):
        chars = ""
        if self.use_digits.get():
            chars += string.digits
        if self.use_letters.get():
            chars += string.ascii_letters
        if self.use_special.get():
            chars += string.punctuation

        if not chars:
            messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов!")
            return

        password = ''.join(random.choice(chars) for _ in range(self.password_length))
        self.password_var.set(password)
        self.save_to_history(password)

    def save_to_history(self, password):
        history = self.load_history_data()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        history.append({
            "password": password,
            "length": self.password_length,
            "timestamp": timestamp
        })
        self.save_history_data(history)
        self.update_history_table()

    def load_history_data(self):
        try:
            with open("password_history.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_history_data(self, history):
        with open("password_history.json", "w") as f:
            json.dump(history, f, indent=2)

    def load_history(self):
        history = self.load_history_data()
        for item in history:
            self.history_tree.insert("", "end", values=(item["password"], item["length"], item["timestamp"]))

    def update_history_table(self):
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        self.load_history()

def main():
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
