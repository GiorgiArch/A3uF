import tkinter as tk
from tkinter import ttk
from tkinter import Button, Entry
from tkinter import messagebox
from functools import partial

class Main_window():


    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.title("A3μF")

        # flag if sub-windows are open
        self.setting_windows_open = False
        self.help_windows_open = False

        # defining geometry
        self.main_window.geometry('600x200')
        self.main_window.resizable(False, False)
        numberofcolumns = 5.
        for i in range(int(numberofcolumns)):
            self.main_window.columnconfigure(i, weight=1)

        # set an icon
        icon_name = "icon.png"
        try:
            self.main_window.tk.call('wm', 'iconphoto', self.main_window._w,\
                tk.PhotoImage(file='./A3uFpy/' + icon_name))
        except:
            print("Program not running from root directory.")
            self.main_window.tk.call('wm', 'iconphoto', self.main_window._w,\
                tk.PhotoImage(file='./'+ icon_name))
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
        self.btn_settings = Button(self.main_window, text="Settings", width = btn_width, command = self.setting_window)
        self.btn_settings.grid(column=2, row=btn_row)
        self.btn_share = Button(self.main_window, text="Share", width = btn_width, state = "disabled")
        self.btn_share.grid(column=3, row=btn_row)
        self.btn_help = Button(self.main_window, text="Help", width = btn_width,\
            command = self.help_window)
        self.btn_help.grid(column=4, row=btn_row)

    def run(self):
        self.main_window.mainloop()

    def error_window(self, message):
        messagebox.showerror('Message title', "%s" % str(message))

    # Help window
    def help_window_close(self):
        self.help_windows_open = False
        self.helpWindow.destroy()

    def help_window(self):
        if not self.help_windows_open:
            self.help_text = "Why are buttons disabled?\nYou need to set the database first in settings."
            self.helpWindow = tk.Toplevel(self.main_window)
            self.helpWindow.protocol("WM_DELETE_WINDOW", self.help_window_close)
            self.helpWindow.title("Help")
            self.helpWindow.geometry("800x600")
            self.helpWindow.resizable(False, False)
            self.helpWindow.columnconfigure(0, weight=1)
            self.help_text = tk.Label(self.helpWindow, text=self.help_text,\
                fg='black', font=("Arial", 20))

            self.help_text.grid(column=0, row=0,sticky="NW", padx = 200)

            # tells the class that the window is open
            self.help_windows_open = True

    # Setting window
    def setting_window_close(self):
        self.setting_windows_open = False
        self.settingWindow.destroy()

    def setting_window(self):
        if not self.setting_windows_open:
            self.settingWindow = tk.Toplevel(self.main_window)
            self.settingWindow.protocol("WM_DELETE_WINDOW", self.setting_window_close)
            self.settingWindow.title("Settings")
            self.settingWindow.geometry("800x600")
            self.settingWindow.resizable(False, False)
            # tells the class that the window is open
            self.setting_windows_open = True
            # partial(self.error_window, "we have no idea")

            self.settingWindow.columnconfigure(0, weight=1)
            self.settingWindow.columnconfigure(1, weight=3)

            current_row = 0

            separator0 = ttk.Separator(self.settingWindow, orient='horizontal')
            separator0.grid(column=0, row=current_row, sticky="ew", pady = 10, columnspan = 5)
            current_row+=1

            self.db_label_title = tk.Label(self.settingWindow, text="Database settings", fg='black', font=("Arial", 16))
            self.db_label_title.grid(column=0, row=current_row, pady = (2,20), sticky="w")
            current_row+=1

            self.btn_db_path = Button(self.settingWindow, text="Path...", width = 5)
            self.btn_db_path.grid(column=2, row=current_row, sticky="w", padx = 5)

            # self.db_label_path = tk.Label(self.settingWindow, text="No path selected", fg='red', font=("Arial", 16))
            self.db_label_path = Entry(self.settingWindow, fg = 'red')
            self.db_label_path.insert(0, "No path selected")
            self.db_label_path.grid(column=1, row=current_row, sticky="ew")

            self.btn_create_db_path = Button(self.settingWindow, text="New...", width = 5)
            self.btn_create_db_path.grid(column=0, row=current_row, sticky="w", padx = 5)

            current_row+=1

            separator1 = ttk.Separator(self.settingWindow, orient='horizontal')
            separator1.grid(column=0, row=current_row, sticky="ew", pady = 20, columnspan = 5)
            current_row+=1
