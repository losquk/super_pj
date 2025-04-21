import math
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import subprocess
import psutil
import time
import random as rd
from file_manager import File_manager
class GUI:
    def __init__(self):
        self.output_file_name = ""
        self.input_file_name = None
        self.alphabet_file_path = None
        self.key = None
        self.block_size = 4
        self.size = int(self.block_size ** 0.5)
        self.matrix = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.selected_coordinates = []
        self.directory = r'D:\dz\GUI'
        self.options = ["ceasar", "rail fence", "cardano", "vigenere"]
        self.new_window = None
        self.buttons = {}

    def initUI(self):
        self.root = tk.Tk()
        self.root.geometry("800x600")
        self.root.title("Шифрування та дешифрування файлів")

        self.file_label = tk.Label(self.root, text="Виберіть файл для шифрування:")
        self.file_label.grid(row=0, column=0)

        self.file_listbox = tk.Listbox(self.root, height=20, width=135)
        self.file_listbox.grid(row=1, column=0)
        self.file_listbox.bind("<<ListboxSelect>>", self.choose_file)

        self.combobox = ttk.Combobox(self.root, values=self.options)
        self.combobox.grid(row=2, column=0, padx=10, pady=10)
        self.combobox.set("Оберіть опцію")
        self.combobox.bind("<<ComboboxSelected>>", self.update_buttons)

        self.setup_widgets()
        self.load_files_from_directory(self.directory)
        self.update_file_list()
        self.root.mainloop()

    def setup_widgets(self):
        self.widgets = {
            "open": tk.Button(self.root, text="Відкрити файл", command=self.open_file),
            "encrypt": tk.Button(self.root, text="Шифрувати файл", command=self.encrypt_button),
            "decrypt": tk.Button(self.root, text="Дешифрувати файл", command=self.decrypt_button),
            "block_size_label": tk.Label(self.root, text="Введіть довжину блоку:"),
            "block_size_entry": tk.Entry(self.root),
            "choose_alphabet": tk.Button(self.root, text="Вибрати алфавіт", command=self.choose_alphabet_file),
            "choose_alphabet_label": tk.Label(self.root, text="Вибраний файл алфавіту:"),
            "key_label": tk.Label(self.root, text="Введіть ключ:"),
            "key_entry": tk.Entry(self.root),
            "output_file_name_label": tk.Label(self.root, text="Назву нового файлу:"),
            "output_file_name": tk.Entry(self.root),
            "Cardano_key": tk.Button(self.root, text="Ввести ключ", command=self.open_new_window)
        }
        for widget in self.widgets.values():
            widget.grid_remove()

    def update_buttons(self, event):
        option = self.combobox.get()
        for widget in self.widgets.values():
            widget.grid_remove()

        display_map = {
            "ceasar": ["block_size_label" , "block_size_entry", "key_label",  "key_entry",  "output_file_name_label",
                        "output_file_name", "open", "encrypt", "decrypt",
                        "choose_alphabet", "choose_alphabet_label"],
            "rail fence": ["block_size_label" , "block_size_entry", "key_label",  "key_entry",  "output_file_name_label",
                        "output_file_name", "open", "encrypt", "decrypt",],
            "cardano": ["Cardano_key", "output_file_name_label", "output_file_name", "open", "encrypt", "decrypt"],
            "vigenere": ["key_label",  "key_entry",  "output_file_name_label",
                        "output_file_name", "open", "encrypt", "decrypt",
                        "choose_alphabet", "choose_alphabet_label"]
        }

        for i, name in enumerate(display_map.get(option, [])):
            self.widgets[name].grid(row=3 + i, column=0, padx=10, pady=5)

    def run_file_operation(self, mode: str):
        option = self.combobox.get()
        if option != "cardano" and option != "vigenere":
            self.block_size = int(self.widgets["block_size_entry"].get())
            self.key = int(self.widgets["key_entry"].get())
        if option == "vigenere":
            self.key = str(self.widgets["key_entry"].get())
            self.block_size = len(self.key)
        self.output_file_name = self.widgets["output_file_name"].get() or f"{mode}ed_" + self.input_file_name
        print(self.input_file_name)
        file_manager = File_manager(self.input_file_name, self.block_size, self.output_file_name, self.alphabet_file_path)
        method = file_manager.file_encrypt if mode == "encrypt" else file_manager.file_decrypt
        method(self.key, option)

    def encrypt_process(self):
        try:
            process = psutil.Process(os.getpid())
            memory_before = process.memory_info().rss
            start_time = time.perf_counter()
            self.run_file_operation("encrypt")
            elapsed_time = time.perf_counter() - start_time
            memory_used = (process.memory_info().rss - memory_before) / (1024 * 1024)
            time.sleep(0.5)
            messagebox.showinfo("Успіх", f"Файл успішно зашифровано: {self.input_file_name}\n"
                                         f"Час виконання: {elapsed_time:.2f} с\n"
                                         f"Використано пам’яті: {memory_used:.2f} МБ")
        except Exception as e:
            messagebox.showerror("Помилка", f"Сталася помилка при шифруванні: {e}")

    def decrypt_process(self):
        try:
            process = psutil.Process(os.getpid())
            memory_before = process.memory_info().rss
            start_time = time.perf_counter()
            self.run_file_operation("decrypt")
            elapsed_time = time.perf_counter() - start_time
            memory_used = (process.memory_info().rss - memory_before) / (1024 * 1024)
            time.sleep(0.5)
            messagebox.showinfo("Успіх", f"Файл успішно дешифровано: {self.input_file_name}\n"
                                         f"Час виконання: {elapsed_time:.2f} с\n"
                                         f"Використано пам’яті: {memory_used:.2f} МБ")
        except Exception as e:
            messagebox.showerror("Помилка", f"Сталася помилка при дешифруванні: {e}")

    def encrypt_button(self):
        if not self.input_file_name:
            messagebox.showerror("Помилка", "Файл не вибрано!")
            return
        if self.combobox.get() == "ceasar" or self.combobox.get() == "vigenere" and not self.alphabet_file_path:
            messagebox.showerror("Помилка", "Файл алфавіту не вибрано для шифру!")
            return
        self.encrypt_process()

    def decrypt_button(self):
        if not self.input_file_name:
            messagebox.showerror("Помилка", "Файл не вибрано!")
            return
        if self.combobox.get() == "ceasar" or self.combobox.get() == "vigenere" and not self.alphabet_file_path:
            messagebox.showerror("Помилка", "Файл алфавіту не вибрано для шифру!")
            return
        self.decrypt_process()

    def load_files_from_directory(self, directory):
        try:
            files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
            for file in files:
                self.file_listbox.insert(tk.END, file)
        except FileNotFoundError:
            messagebox.showerror("Помилка", f"Директорія {directory} не знайдена!")

    def update_file_list(self):
        current_files = set(self.file_listbox.get(0, tk.END))
        new_files = {f for f in os.listdir() if f.endswith('.txt')}
        if current_files != new_files:
            self.file_listbox.delete(0, tk.END)
            for file in sorted(new_files):
                self.file_listbox.insert(tk.END, file)
        self.root.after(2000, self.update_file_list)

    def choose_file(self, event):
        try:
            filename = self.file_listbox.get(self.file_listbox.curselection())
            self.input_file_name = filename
            self.file_label.config(text=f"Вибраний файл: {self.input_file_name}")
            print(f"[DEBUG] Обрано файл: {self.input_file_name}")
        except IndexError:
            messagebox.showerror("Помилка", "Будь ласка, виберіть файл зі списку.")

    def choose_alphabet_file(self):
        self.alphabet_file_path = filedialog.askopenfilename(title="Виберіть файл для алфавіту",
                                                             filetypes=[("Text files", "*.txt")])
        if self.alphabet_file_path:
            self.widgets["choose_alphabet_label"].config(text=f"Вибрано файл алфавіту: {os.path.basename(self.alphabet_file_path)}")

    def load_cardano_key(self):
        key_path = filedialog.askopenfilename(title="Виберіть файл ключа Кардано", filetypes=[("Text files", "*.txt")])
        if not key_path:
            return

        try:
            self.key = File_manager.load_cardano_key(key_path)
            max_i = max(coord[0] for coord in self.key)
            max_j = max(coord[1] for coord in self.key)
            self.size = max(max_i, max_j) + 1
            self.block_size = self.size ** 2
            if hasattr(self, "size_combobox"):
                self.size_combobox.set(str(self.size))
            self.create_matrix()
            self.selected_coordinates.clear()
            for i, j in self.key:
                if self.matrix[i][j] == 0:
                    self.toggle_cell(i, j)
            messagebox.showinfo("Успіх", "Ключ успішно завантажено з файлу!")
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося завантажити ключ: {e}")

    def open_file(self):
        if self.input_file_name:
            subprocess.run(["notepad", self.input_file_name])
        else:
            messagebox.showerror("Помилка", "Файл не вибрано!")

    def open_new_window(self):
        if self.new_window is None or not self.new_window.winfo_exists():
            self.new_window = tk.Toplevel(self.root)
            self.new_window.geometry("800x600")
            self.new_window.title("Ключ для шифру Кардано")

            self.dropdown_frame = tk.Frame(self.new_window)
            self.dropdown_frame.pack(pady=10)
            self.create_dropdown()

            self.matrix_frame = tk.Frame(self.new_window)
            self.matrix_frame.pack(pady=10)
            self.create_matrix()

            self.remaining_label = tk.Label(
                self.new_window,
                text=f"Вибрано: {len(self.selected_coordinates)} | Потрібно: {math.ceil(self.size**2 / 4)}"
            )
            self.remaining_label.pack(pady=5)

            save_button = tk.Button(self.new_window, text="Зберегти ключ", command=self.Cardano_key)
            save_button.pack(pady=10)
            generate_key = tk.Button(self.new_window, text="згенерувати ключ", command=self.random_Cardano_key)
            generate_key.pack(pady = 10)
            load_button = tk.Button(self.new_window, text="Завантажити ключ з файлу", command=self.load_cardano_key)
            load_button.pack(pady=10)
            close_button = tk.Button(self.new_window, text="Закрити", command=self.new_window.destroy)
            close_button.pack(pady=10)
        else:
            print("Вікно вже відкрите!")

    def random_Cardano_key(self):
        import random as rd
        self.size = int(self.size_combobox.get())
        self.block_size = self.size ** 2
        self.selected_coordinates.clear()
        self.key = []
        banned = []

        self.create_matrix()
        while len(self.key) < math.ceil(self.block_size / 4):
            j = rd.randint(0, self.size - 1)
            i = rd.randint(0, self.size - 1)
            rotations = self.rotate_coordinates(i, j) + [[i, j]]
            if all(coord not in banned for coord in rotations):
                self.key.append([i, j])
                banned.extend(rotations)
                self.toggle_cell(i, j)
                i+= 1
    def create_dropdown(self):
        tk.Label(self.dropdown_frame, text="Розмір матриці:").pack(side="left")
        options = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
        self.size_var = tk.IntVar(value=self.size)
        self.size_combobox = ttk.Combobox(self.dropdown_frame, values=options, width=3)
        self.size_combobox.current(options.index(self.size))
        self.size_combobox.pack(side="left")
        self.size_combobox.bind("<<ComboboxSelected>>", self.update_matrix)

    def create_matrix(self):
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()

        self.matrix = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.buttons = {}


        button_width = max(2, int(8 - self.size * 0.3))
        button_height = max(1, int(4 - self.size * 0.2))

        for i in range(self.size):
            for j in range(self.size):
                button = tk.Button(
                    self.matrix_frame,
                    text=" ",
                    width=button_width,
                    height=button_height,
                    command=lambda i=i, j=j: self.toggle_cell(i, j)
                )
                button.grid(row=i, column=j, padx=1, pady=1)
                self.buttons[(i, j)] = button

    def update_matrix(self, event=None):
        self.size = int(self.size_combobox.get())
        self.block_size = self.size ** 2
        self.create_matrix()
        if hasattr(self, "remaining_label"):
            self.remaining_label.config(
                text=f"Вибрано: {len(self.selected_coordinates)} | Потрібно: {math.ceil(self.block_size / 4)}"
            )

    def rotate_coordinates(self, i, j):
        return [[j, self.size - 1 - i], [self.size - 1 - i, self.size - 1 - j], [self.size - 1 - j, i]]

    def toggle_cell(self, i, j):
        if self.matrix[i][j] == 0:
            self.matrix[i][j] = 1
            self.buttons[(i, j)].config(bg="green", state="normal")
            self.selected_coordinates.append((i, j))
            for x, y in self.rotate_coordinates(i, j):
                if self.matrix[x][y] == 0:
                    self.matrix[x][y] = -1
                    self.buttons[(x, y)].config(bg="red", state="disabled")
        elif self.matrix[i][j] == 1:
            self.matrix[i][j] = 0
            self.buttons[(i, j)].config(bg="SystemButtonFace", state="normal")
            if (i, j) in self.selected_coordinates:
                self.selected_coordinates.remove((i, j))
            for x, y in self.rotate_coordinates(i, j):
                if self.matrix[x][y] == -1:
                    self.matrix[x][y] = 0
                    self.buttons[(x, y)].config(bg="SystemButtonFace", state="normal")
        if hasattr(self, "remaining_label"):
            self.remaining_label.config(
                text=f"Вибрано: {len(self.selected_coordinates)} | Потрібно: {math.ceil(self.block_size / 4)}"
            )

    def Cardano_key(self):
        if len(self.selected_coordinates) < math.ceil(self.block_size / 4):
            messagebox.showerror("Помилка", "Замало дірок")
            return
        self.key = self.selected_coordinates
        messagebox.showinfo("Ключ", f"Ключ збережено: {self.key}")
        self.new_window.destroy()

if __name__ == "__main__":
    gui = GUI()
    gui.initUI()
