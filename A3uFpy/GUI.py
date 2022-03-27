import tkinter as tk


class Main_window():
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.title("A3μF")
        self.main_window.geometry('600x600')
        self.title = tk.Label(self.main_window, text="Welcome to A3μF", fg='black', font=("Arial Bold", 50))
        self.title.grid(column=0, row=0)
        self.subtitle = tk.Label(self.main_window, text="Automatic Analysis of Archaeological Micro-Fauna",\
            fg='black', font=("Arial", 20))
        self.subtitle.grid(column=0, row=1)

    def run(self):
        self.main_window.mainloop()
