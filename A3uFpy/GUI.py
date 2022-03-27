import tkinter as tk


class Main_window():
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.title("A3μF")
        self.main_window.geometry('600x600')
        self.lbl = tk.Label(self.main_window, text="Welcome to A3μF", bg='red', fg='white', font=("Arial Bold", 50))
        self.lbl.grid(column=0, row=0)

    def run(self):
        self.main_window.mainloop()
