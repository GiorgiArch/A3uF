import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import Button, Entry
from tkinter import filedialog
from tkinter.filedialog import askopenfile, askopenfilename
from tkinter import messagebox
import tkinter.font as tkFont
from functools import partial
import os,ctypes
from instrument_DAq import Microscope, Scale
from tkhtmlview import HTMLLabel
from help import main_help,instrumentation_help


class Main_window():

    def __init__(self, microscope_controller, scale_controller):
        # instrument classes
        self.microscope_controller = microscope_controller
        self.in_use_microscope = None
        # instrument handling
        self.microscope = None
        self.camera_OK = False
        self.available_microscopes = ["Click refresh"]

        self.scale_controller = scale_controller
        self.in_use_scale = None
        self.scales = None
        self.scale_OK = False
        self.available_scales = ["Click refresh"]

        self.main_window = tk.Tk()
        self.main_window.title("A3μF")

        # flag if sub-windows are open
        self.setting_windows_open = False
        self.help_windows_open = False
        self.instrumentation_help_window_open = False
        self.database_path = ''
        if os.name == 'nt':
            self.text_scaler_title = 0.8
        else:
            self.text_scaler_title = 1

        self.std_font = tkFont.Font(family='Arial', size=16)
        s = ttk.Style()
        s.configure('.', font=self.std_font)
        # defining geometry
        if os.name == 'nt':
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
            self.main_window.tk.call('tk', 'scaling', 3.0)
            self.main_window_size = '1800x600'
            self.setting_window_size = '1800x1600'
            self.help_window_size = "1800x1800"
        else:
            # self.main_window_size = '600x200'
            # self.setting_window_size = '600x533'
            # self.help_window_size = "600x800"
            # check on macos
            self.main_window_size = '1800x600'
            self.setting_window_size = '1800x1600'
            self.help_window_size = "1800x1800"
        self.main_window.geometry(self.main_window_size)
        # self.main_window.tk.call('tk', 'scaling', 2.0)
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
        self.font = tkFont.Font(family='Arial', size=int(20*self.text_scaler_title))
        self.font_bold = tkFont.Font(family='Arial Bold', size=int(50*self.text_scaler_title))
        self.title = tk.Label(self.main_window, text="Welcome to A3μF", fg='blue', font=self.font_bold)
        self.title.grid(column=0, row=0, columnspan = 6)
        self.subtitle = tk.Label(self.main_window, text="Automatic Analysis of Archaeological Micro-Fauna",\
            fg='black', font=self.font)
        self.subtitle.grid(column=0, row=1, columnspan = 6)

        # defining buttons
        btn_width = 10
        btn_row = 2
        self.main_window.rowconfigure(btn_row, pad=50)
        for i in range(6):
            self.main_window.columnconfigure(i, pad=50, weight = 1)
        self.btn_analysis = Button(self.main_window, text="Analysis", width = btn_width, state = "disabled")
        self.btn_analysis.grid(column=0, row=btn_row)
        self.btn_database = Button(self.main_window, text="Database", width = btn_width, state = "disabled")
        self.btn_database.grid(column=1, row=btn_row)
        self.btn_measure = Button(self.main_window, text="Measure", width = btn_width, state = "disabled")
        self.btn_measure.grid(column=2, row=btn_row)
        self.btn_settings = Button(self.main_window, text="Settings", width = btn_width, command = self.setting_window)
        self.btn_settings.grid(column=3, row=btn_row)
        self.btn_share = Button(self.main_window, text="Share", width = btn_width, state = "disabled")
        self.btn_share.grid(column=4, row=btn_row)
        self.btn_help = Button(self.main_window, text="Help", width = btn_width,\
            command = self.help_window)
        self.btn_help.grid(column=5, row=btn_row)

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
            self.helpWindow = tk.Toplevel(self.main_window)
            self.helpWindow.protocol("WM_DELETE_WINDOW", self.help_window_close)
            self.helpWindow.title("Help")
            self.helpWindow.geometry(self.help_window_size)
            self.helpWindow.resizable(False, False)

            self.helpWindow.columnconfigure(0, weight=1)
            self.helpWindow.rowconfigure(0, weight=1)

            self.help_text = HTMLLabel(self.helpWindow , html=main_help)
            self.help_text.grid(column=0, row=0,sticky="nsew",padx= 10, pady = 10)
            # Create a vertical scrollbar linked to the canvas.
            vsbar = tk.Scrollbar(self.helpWindow, orient=tk.VERTICAL, command=self.help_text.yview)
            vsbar.grid(row=0, column=1, sticky=tk.NS)

            # tells the class that the window is open
            self.help_windows_open = True

    def instrumentation_help_window_close(self):
        self.instrumentation_help_window_open = False
        self.instrumentation_help_window.destroy()

    def Instrumentation_help_window(self):
        if not self.instrumentation_help_window_open:
            self.instrumentation_help_window = tk.Toplevel(self.settingWindow)
            self.instrumentation_help_window.protocol("WM_DELETE_WINDOW", self.instrumentation_help_window_close)
            self.instrumentation_help_window.title("Help")
            self.instrumentation_help_window.geometry(self.help_window_size)
            self.instrumentation_help_window.resizable(False, False)

            self.instrumentation_help_window.columnconfigure(0, weight=1)
            self.instrumentation_help_window.rowconfigure(0, weight=1)

            self.help_text_instrumentation = HTMLLabel(self.instrumentation_help_window , html=instrumentation_help)
            self.help_text_instrumentation.grid(column=0, row=0,sticky="nsew",padx= 10, pady = 10)
            # Create a vertical scrollbar linked to the canvas.
            vsbar = tk.Scrollbar(self.instrumentation_help_window, orient=tk.VERTICAL, command=self.help_text_instrumentation.yview)
            vsbar.grid(row=0, column=1, sticky=tk.NS)

            # tells the class that the window is open
            self.instrumentation_help_window_open = True

    # Setting window


    def setting_window_close(self):
        self.setting_windows_open = False
        self.settingWindow.destroy()

    def check_file(self, filename):
        # TODO integrate database check
        if os.path.splitext(filename)[1] == ".py":
            return True
        else:
            return False

    def open_file(self):
        filename = filedialog.askopenfilename(filetypes=[('All Files', '*.*', '')])
        self.db_label_path.delete(0, END)
        if self.check_file(filename):
            self.db_label_path.insert(0, filename)
            self.db_label_path['fg'] = 'green'
            self.database_path = filename
        elif filename == '':
            self.db_label_path.insert(0, "No path selected")
            self.db_label_path['fg'] = 'red'
        else:
            self.db_label_path.insert(0, "Invalid file")
            self.db_label_path['fg'] = 'red'
            self.database_path = ''

    def check_db_valid(self):
        '''
        Check if the database is valid TODO update with db checker
        '''
        if self.database_path == '':
            self.error_window("No database selected")
        else:
            with open(self.database_path,"r") as f:
                dd = len(f.readlines())
                messagebox.showinfo('Message title', "file long: %d" % dd)

    def refresh_microscope_list(self):
        self.available_microscopes = self.microscope_controller.list_cams()
        # menu = self.microscope_selector["menu"]
        self.microscope_selector["menu"].delete(0, "end")
        # menu.delete(0, "end")
        for string in self.available_microscopes:
            self.microscope_selector["menu"].add_command(label=string,
                 command=lambda value=string: self.selected_microscopes.set(value)
             )

    def test_microscope(self):
        """
        Test the microscope
        """
        if self.in_use_microscope is not None:
            err = self.microscope_controller.test_cam()
            if err is not None:
                self.error_window(err)
        else:
            self.error_window("No microscope selected")

        return

    def select_microscope(self, *args):
        """
        Just select a microscope
        """
        try:
            sel = self.selected_microscopes.get()
            self.in_use_microscope = self.available_microscopes.index(sel)
        except:
            self.error_window("Could not select the microscope")
        err = self.microscope_controller.select_cam(self.in_use_microscope)
        if err is not None:
            self.error_window(err)
        print("Selecting microscope %s"%sel)

    def select_scale(self, *args):
        """
        Select a scale
        """
        try:
            sel = self.selected_scales.get()
            self.in_use_scale = sel
        except:
            self.error_window("Could not select the scale")
            # print(self.in_use_scale)
        err = self.scale_controller.initialize(self.in_use_scale)
        if err is not None:
            self.error_window(err)
        print("Selecting scale %s\n"%sel)
    def confirm_select_microscope(self):
        """
        Confirm selection and change the behaviour of the setting window to show that a microscope has been selected.
        """

        message = "Camera not ready or calibration not present"
        if self.microscope_controller.initialized and (self.microscope_controller.calibration is not None):
            messagebox.showinfo("Camera", "Camera connected")
            self.camera_OK = True
            self.btn_microscope_finder.configure(bg = "green")
        else:
            messagebox.showerror('Camera', "%s" % str(message))
            self.btn_microscope_finder.configure(bg = "red")
            self.camera_OK = False

    def confirm_select_scale(self):
        """
        Confirm selection and change the behaviour of the setting window to show that a microscope has been selected.
        """
        message = "Scale not ready"
        if self.scale_controller.initialized:
            messagebox.showinfo("Scale", "Scale connected")
            self.btn_scale_finder.configure(bg = "green")
            self.scale_OK = True
        else:
            messagebox.showerror('Scale', "%s" % str(message))
            self.btn_scale_finder.configure(bg = "red")
            self.scale_OK = False

    def refresh_scale_list(self):
        '''
        looks for scales and refresh menu
        '''
        self.available_scales = self.scale_controller.list_available_scales()
        if self.available_scales=="OS is blocking access to the port or no device connected":
            self.available_scales = []
            messagebox.showerror('Scale', "OS is blocking access to the port or no device connected")
        # menu = self.microscope_selector["menu"]
        self.scale_selector["menu"].delete(0, "end")
        # menu.delete(0, "end")
        for string in self.available_scales:
            self.scale_selector["menu"].add_command(label=string,
                 command=lambda value=string: self.selected_scales.set(value)
             )

    def test_scale(self):
        '''
        Take a measurement of the scales and display in a pop up.
        '''
        try:
            value = self.scale_controller.read()
        except Exception as e:
            text = str(e)
        if value is None:
            text = "Cannot get a value from the scale, DAq error. is the scale connected?"

        else:
            text = "Result: %.2f mg" % value
        messagebox.showinfo("Scale test", text)

    def setting_window(self):
        if not self.setting_windows_open:
            self.settingWindow = tk.Toplevel(self.main_window)
            self.settingWindow.protocol("WM_DELETE_WINDOW", self.setting_window_close)
            self.settingWindow.title("Settings")
            self.settingWindow.geometry(self.setting_window_size)
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
            # database setting section with buttons and path finder

            self.db_label_title = tk.Label(self.settingWindow, text="Database settings", fg='blue', font=self.font)
            self.db_label_title.grid(column=0, row=current_row, pady = 5, sticky="w")
            current_row+=1

            self.btn_db_path = Button(self.settingWindow, text="Path...", width = 5, command = self.open_file)
            self.btn_db_path.grid(column=2, row=current_row, sticky="w", padx = 5)


            # self.db_label_path = tk.Label(self.settingWindow, text="No path selected", fg='red', font=("Arial", 16))
            if not self.check_file(self.database_path):
                self.db_label_path = Entry(self.settingWindow, fg = 'red')
                self.db_label_path.insert(0, "No path selected")
            else:
                self.db_label_path = Entry(self.settingWindow, fg = 'green')
                self.db_label_path.insert(0, self.database_path)

            self.db_label_path.grid(column=1, row=current_row, sticky="ew")


            self.btn_create_db_path = Button(self.settingWindow, text="New...", width = 5)
            self.btn_create_db_path.grid(column=0, row=current_row, sticky="w", padx = 5)

            current_row+=1


            self.btn_check_db = Button(self.settingWindow, text="Check", width = 5, command = self.check_db_valid)
            self.btn_check_db.grid(column=1, row=current_row, sticky="w", padx = 0)
            current_row+=1

            self.btn_db_help = Button(self.settingWindow, text="Help", width = 5)
            self.btn_db_help.grid(column=2, row=current_row, sticky="w", padx = 0)
            current_row+=1

            separator1 = ttk.Separator(self.settingWindow, orient='horizontal')
            separator1.grid(column=0, row=current_row, sticky="ew", pady = 20, columnspan = 5)
            current_row+=1

            self.sett_lbl_title = tk.Label(self.settingWindow, text="Instrumentation settings", fg='blue', font=self.font)
            self.sett_lbl_title.grid(column=0, row=current_row, pady = 5, columnspan = 5, sticky="w")
            current_row+=1

            if self.camera_OK:
                camera_bg = 'green'
            else:
                camera_bg = 'red'

            self.btn_microscope_finder = Button(self.settingWindow, text="Connect Microscope", width = 20,\
                command = self.confirm_select_microscope, bg=camera_bg)
            self.btn_microscope_finder.grid(column=0, row=current_row, sticky="w", padx = 30)

            # check for microscopes

            self.selected_microscopes = StringVar()
            if self.in_use_microscope is None:
                self.selected_microscopes.set( "Select microscope" )
            else:
                self.selected_microscopes.set( self.available_microscopes[self.in_use_microscope])
            self.microscope_selector = OptionMenu(
                self.settingWindow,
                self.selected_microscopes,
                *self.available_microscopes,
                # command = self.select_microscope
            )
            self.selected_microscopes.trace("w", self.select_microscope)
            self.microscope_selector.grid(column=1, row=current_row, sticky="ew", padx = 5)

            self.btn_microscope_test = Button(self.settingWindow, text="Test Microscope", width = 15, command = self.test_microscope)
            self.btn_microscope_test.grid(column=2, row=current_row, sticky="w", padx = 5, pady = 25)

            self.btn_microscope_refresh = Button(self.settingWindow, text="Refresh list", width = 15, command = self.refresh_microscope_list)
            self.btn_microscope_refresh.grid(column=3, row=current_row, sticky="w", padx = 5, pady = 25)

            current_row+=1

            if self.scale_OK:
                scale_bg = 'green'
            else:
                scale_bg = 'red'

            self.btn_scale_finder = Button(self.settingWindow, text="Connect Scale", width = 20, command = self.confirm_select_scale, bg = scale_bg)
            self.btn_scale_finder.grid(column=0, row=current_row, sticky="w", padx = 30, pady = 25)


            self.selected_scales = StringVar()
            if self.in_use_scale is None:
                self.selected_scales.set( "Select scale" )
            else:
                self.selected_scales.set( self.in_use_scale)

            self.scale_selector = OptionMenu( self.settingWindow, self.selected_scales, *self.available_scales)
            self.scale_selector.grid(column=1, row=current_row, sticky="ew", padx = 5, pady= 10)
            self.selected_scales.trace("w", self.select_scale)

            self.btn_scale_test = Button(self.settingWindow, text="Test Scale", width = 15, command = self.test_scale)
            self.btn_scale_test.grid(column=2, row=current_row, sticky="w", padx = 5, pady = 25)

            self.btn_scale_refresh = Button(self.settingWindow, text="Refresh list", width = 15, command = self.refresh_scale_list)
            self.btn_scale_refresh.grid(column=3, row=current_row, sticky="w", padx = 5, pady = 25)


            current_row+=1

            self.btn_instr_help = Button(self.settingWindow, text="Help", width = 5, command = self.Instrumentation_help_window)
            self.btn_instr_help.grid(column=2, row=current_row, sticky="w", padx = 0)
            current_row+=1
          # buttons in this section should scan for USB
