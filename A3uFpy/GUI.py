import tkinter as tk
from tkinter import Button


class Main_window():


    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.title("A3μF")

        # flag if sub-windows are open
        self.help_windows_open = False

        # defining geometry
        self.main_window.geometry('600x200')
        numberofcolumns = 5.
        for i in range(int(numberofcolumns)):
            self.main_window.columnconfigure(i, weight=1)

        # set an icon
        try:
            self.main_window.tk.call('wm', 'iconphoto', self.main_window._w,\
                tk.PhotoImage(file='./A3uFpy/Test_icon.png'))
        except:
            print("Program not running from root directory.")
            self.main_window.tk.call('wm', 'iconphoto', self.main_window._w,\
                tk.PhotoImage(file='./Test_icon.png'))
       #window appearence
        self.title = tk.Label(self.main_window, text="Welcome to A3μF", fg='blue', font=("Arial Bold", 50))
        self.title.grid(column=0, row=0, columnspan = 5)
        self.subtitle = tk.Label(self.main_window, text="Automatic Analysis of Archaeological Micro-Fauna",\
            fg='black', font=("Arial", 20))
        self.subtitle.grid(column=0, row=1, columnspan = 5)

        # defining buttons
        btn_width = 10
        btn_row = 2
        self.main_window.rowconfigure(btn_row, pad=50)
        self.btn_analysis = Button(self.main_window, text="Analysis", width = btn_width, state = "disabled")
        self.btn_analysis.grid(column=0, row=btn_row)
        self.btn_database = Button(self.main_window, text="Database", width = btn_width, state = "disabled")
        self.btn_database.grid(column=1, row=btn_row)
        self.btn_settings = Button(self.main_window, text="Settings", width = btn_width)
        self.btn_settings.grid(column=2, row=btn_row)
        self.btn_share = Button(self.main_window, text="Share", width = btn_width, state = "disabled")
        self.btn_share.grid(column=3, row=btn_row)
        self.btn_help = Button(self.main_window, text="Help", width = btn_width,\
            command = self.help_window)
        self.btn_help.grid(column=4, row=btn_row)
# how windows work
    def run(self):
        self.main_window.mainloop()

    def help_window_close(self):
        self.help_windows_open = False
        self.helpWindow.destroy()

    def help_window(self):
        if not self.help_windows_open:
            self.help_text = "Why are buttons disabled?\You need to set the database first in settings."
            self.helpWindow = tk.Toplevel(self.main_window)
            self.helpWindow.protocol("WM_DELETE_WINDOW", self.help_window_close)
            self.helpWindow.title("Help")
            self.helpWindow.geometry("800x600")
            self.help_text = tk.Label(self.helpWindow, text=self.help_text,\
                fg='black', font=("Arial", 20))
            self.help_text.grid(column=0, row=0)

            # tells the class that the window is open
            self.help_windows_open = True
