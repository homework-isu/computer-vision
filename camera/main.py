from typing import List
import tkinter as tk
from tkinter import ttk, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from matplotlib.figure import Figure
import numpy as np


class App:
    object: np.array
    row: int
    start_screen: tk.Tk
    main_screen: tk.Tk


    def __init__(self):
        self.object = np.array([])
        self.row = 0
        self.start_screen = tk.Tk()

        self.set_new_screen(self.start_screen, "Выбор файла", "400x300")

        self.init_app()

    def init_app(self):
        button = tk.Button(self.start_screen, text="Выберите файл", command=self.read_from_file)
        button.pack(pady=(self.start_screen.winfo_reqheight() - button.winfo_reqheight()) / 2)

    def set_new_screen(self, root: tk.Tk, title: str, geometry: str):
        root.title(title)
        if geometry != "":
            root.geometry(geometry)

    def read_from_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])

        if file_path:
            sub_obj = []
            with open(file_path, 'r') as f:
                for s in f:
                    s += ' 1'
                    sub_obj.append(s.split())

            self.object = np.array(sub_obj).astype(float)
            self.start_screen.withdraw()  # Скрыть основное окно
            self.main_app()

    def extract_values(self):
        return {
            "zfar": float(self.Zfar_slider.get()),
            "znear": float(self.Znear_slider.get()),
            "dx": float(self.dX_slider.get()),
            "dy": float(self.dY_slider.get()),
            "camx": float(self.camx_slider.get()),
            "camy": float(self.camy_slider.get()),
            "angle": np.radians(float(self.XY_slider.get())),
            "K1": float(self.K1_slider.get())
        }

    def update_frame(self):
        values = self.extract_values()

        Zrange = values["zfar"] - values["znear"]

        dots_center = np.array([0.1, 0.1])

        cos_val = np.cos(values["angle"])
        sin_val = np.sin(values["angle"])

        if Zrange == 0:
            Zrange = 1

        P = np.array(
            [[cos_val, -sin_val, values["dx"], 0], [sin_val, cos_val, values["dy"], 0], [0, 0, -values["zfar"] / Zrange, values["znear"] * values["zfar"] / Zrange],
             [0, 0, 1, 0]])
        Cam = np.array([[values["camx"], 0, 0, 0], [0, values["camy"], 0, 0], [0, 0, 1, 0]])
        dots = []

        for i in range(self.object.shape[0]):
            f = Cam @ P @ self.object[i, :]
            if f[2] == 0:
                dots.append(f)
                continue
            dots.append(f / f[2])
        dots = np.array(dots)

        r = (dots[:, :2] - dots_center) ** 2

        f1 = (r).sum(axis=1)
        f2 = (r ** 2).sum(axis=1)

        mask = np.expand_dims(values["K1"] * f1 + 0.0 * f2, axis=-1)
        dots_new = (dots[:, :2]) + (dots[:, :2] - dots_center) * mask

        self.ax.clear()
        self.ax.plot(dots_new[:, 0], dots_new[:, 1], '-D')
        self.canvas.draw()

    def update_from_entry(self, entry, slider):
        try:
            value = float(entry.get())
            slider.set(value)
            self.update_frame()
        except ValueError:
            pass

    def update_from_slider(self, slider, entry):
        value = slider.get()
        entry.delete(0, tk.END)
        entry.insert(0, str(value))
        self.update_frame()

    def select_all(self, event):
        event.widget.icursor(0)
        event.widget.select_range(0, 'end')

    def reset_values(self):
        self.XY_entry.delete(0, tk.END)
        self.XY_entry.insert(0, "0.0")

        self.Zfar_entry.delete(0, tk.END)
        self.Zfar_entry.insert(0, "-10.0")

        self.Znear_entry.delete(0, tk.END)
        self.Znear_entry.insert(0, "-3.0")

        self.dX_entry.delete(0, tk.END)
        self.dX_entry.insert(0, "-0.2")

        self.dY_entry.delete(0, tk.END)
        self.dY_entry.insert(0, "-0.5")

        self.camx_entry.delete(0, tk.END)
        self.camx_entry.insert(0, "1.0")

        self.camy_entry.delete(0, tk.END)
        self.camy_entry.insert(0, "1.0")

        self.K1_entry.delete(0, tk.END)
        self.K1_entry.insert(0, "1.0")

        self.apply_values()

    def apply_values(self):
        try:
            XY = float(self.XY_entry.get())
            self.XY_slider.set(XY)

            Zfar = float(self.Zfar_entry.get())
            self.Zfar_slider.set(Zfar)

            Znear = float(self.Znear_entry.get())
            self.Znear_slider.set(Znear)

            dX = float(self.dX_entry.get())
            self.dX_slider.set(dX)

            dY = float(self.dY_entry.get())
            self.dY_slider.set(dY)

            camx = float(self.camx_entry.get())
            self.camx_slider.set(camx)

            camy = float(self.camx_entry.get())
            self.camy_slider.set(camy)

            K1 = float(self.K1_entry.get())
            self.K1_slider.set(K1)
            self.update_frame()
        except ValueError:
            pass

    def create(self, name, original_meaning="0.0", from_=0, to=10):

        label = ttk.Label(self.center_frame, text=name)
        min_label = ttk.Label(self.center_frame, text=f"{from_}")
        max_label = ttk.Label(self.center_frame, text=f"{to}")
        label.grid(row=self.row, column=0, padx=10, pady=5)
        min_label.grid(row=self.row, column=1, padx=5, pady=5)
        slider = ttk.Scale(self.center_frame, from_=from_, to=to, command=lambda x: self.update_from_slider(slider, entry))
        slider.grid(row=self.row, column=2, padx=10, pady=5)
        max_label.grid(row=self.row, column=3, padx=5, pady=5)
        entry = ttk.Entry(self.center_frame)
        entry.grid(row=self.row, column=4, padx=10, pady=5)
        entry.insert(0, original_meaning)
        entry.bind("<FocusIn>", self.select_all)

        slider.bind("<ButtonRelease-1>", lambda event: self.update_from_entry(entry, slider))
        entry.bind("<Return>", lambda event: self.update_from_entry(entry, slider))
        self.row += 1

        return label, slider, entry

    def main_app(self):
        self.main_screen = tk.Tk()
        self.set_new_screen(self.main_screen, "График с ползунками и текстовыми полями", "")

        frame = ttk.Frame(self.main_screen)
        frame.grid(row=0, column=0, pady=10, padx=10)

        fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(fig, master=frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.center_frame = ttk.Frame(self.main_screen)
        self.center_frame.grid(row=1, column=0, padx=10, pady=10)
        self.center_frame.columnconfigure(0, weight=1)

        self.XY_label, self.XY_slider, self.XY_entry = self.create(name="Повороты в плоскости XY:", original_meaning="0.0", from_=-180, to=180)

        self.Zfar_label, self.Zfar_slider, self.Zfar_entry = self.create(name="Zfar:", original_meaning="-10.0", from_=-10, to=10)
        self.Znear_label, self.Znear_slider, self.Znear_entry = self.create("Znear:", original_meaning="-3.0", from_=-10, to=10)
        self.dX_label, self.dX_slider, self.dX_entry = self.create("dX:", original_meaning="-0.2", from_=-10, to=10)
        self.dY_label, self.dY_slider, self.dY_entry = self.create("dY:", original_meaning="-0.5", from_=-10, to=10)

        self.camx_label, self.camx_slider, self.camx_entry = self.create("cam x:", original_meaning="1.0", from_=-10, to=10)
        self.camy_label, self.camy_slider, self.camy_entry = self.create("cam y:", original_meaning="1.0", from_=-10, to=10)

        self.K1_label, self.K1_slider, self.K1_entry = self.create("K1:", original_meaning="1.0", from_=-10, to=10)

        self.apply_values()

        apply_button = ttk.Button(self.main_screen, text="Применить", command=self.apply_values)
        apply_button.grid(row=2, column=0, padx=10, pady=5)

        reset_button = ttk.Button(self.main_screen, text="Сбросить", command=self.reset_values)
        reset_button.grid(row=3, column=0, padx=10, pady=5)

        self.update_frame()

        self.loop()

    def loop(self):
        return self.start_screen.mainloop()


app = App()
app.loop()