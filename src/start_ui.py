
import string
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as tkfont

from src.password_ui import PasswordUI



class StartUI(tk.Tk):


    def __init__(self, user):

        super().__init__()
        self._user = user

        self.title("Math Facts")
        self.attributes('-type', 'dialog')

        self._padding = 4
        self._boarderwidth = 3

        default_font = tkfont.nametofont("TkDefaultFont")
        self._big_font = tkfont.Font(family=default_font.actual()["family"], size=42, weight="bold")
        self._med_font = tkfont.Font(family=default_font.actual()["family"], size=14)
        self._small_font = tkfont.Font(family=default_font.actual()["family"], size=12)
        
        self._combobox: ttk.Combobox
        self._main_button_text = tk.StringVar(value="Start")
        self._combobox_text = tk.StringVar(value="Select User")

        self._main_frame = tk.Frame(self)
        self._make_layout(self._main_frame)
        self._main_frame.pack(expand=True, fill='both', padx=4, pady=4)


    def _make_layout(self, parent):

        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_rowconfigure(1, weight=1)

        welcome_frame = tk.Frame(parent, bd=self._boarderwidth, relief="groove")
        widgets_frame = tk.Frame(parent)

        welcome_frame.grid(row=0, column=0, sticky='nsew', padx=self._padding, pady=self._padding)
        widgets_frame.grid(row=1, column=0, sticky='nsew', padx=self._padding, pady=self._padding)

        self._welcome_frame(welcome_frame)
        self._widgets_frame(widgets_frame)


    def _welcome_frame(self, parent):

        frame = tk.Frame(parent)
        frame.pack(expand=True, fill='both')

        message = "Welcome to Math Facts!"
        title_label = tk.Label(frame, text=message, font=self._big_font)
        title_label.pack(fill='both', expand=True, padx=18, pady=self._padding)


    def _widgets_frame(self, parent):

        frame = tk.Frame(parent)
        frame.pack(expand=True, fill='both', pady=self._padding)

        style = ttk.Style(self)
        style.configure('TButton', font=self._med_font, padding=10)

        main_button = ttk.Button(frame, text="⚙", style='TButton', command=self._on_settings_clicked, width=3)
        cancel_button = ttk.Button(frame, textvariable=self._main_button_text, style='TButton', command=self._on_main_clicked, width=10)
        self._combobox = ttk.Combobox(
            frame, values=self._user.get_usernames(), state="normal", 
            font=self._med_font, textvariable=self._combobox_text)
        
        main_button.pack(side='right', fill='y', padx=self._padding)
        cancel_button.pack(side='right', fill='y', padx=self._padding)
        self._combobox.pack(side='right', fill='y', padx=self._padding)
        self._combobox_text.trace_add('write', self._on_user_update)


    def _on_settings_clicked(self):

        cbbox_val = self._combobox_text.get()
        if not cbbox_val or cbbox_val == "Select User":
            return

        if cbbox_val in self._user.get_usernames():
            self._user.load_user(cbbox_val)
        else:
            return
        PasswordUI(self._user)


    def _on_main_clicked(self):

        cbbox_val = self._combobox_text.get()
        if not cbbox_val or cbbox_val == "Select User":
            return
        
        if self._main_button_text.get() == "Create":
            self._on_create_clicked()
            return
        elif self._main_button_text.get() == "Start":
            self._on_start_clicked()
            return
    

    def _on_user_update(self, *_):

        cbbox_val = self._combobox_text.get()

        if cbbox_val not in self._user.get_usernames():
            self._main_button_text.set("Create")
        else:
            self._main_button_text.set("Start")


    def _on_create_clicked(self):

        cbbox_val = self._combobox.get()

        errs = []
        if not cbbox_val[0].isalpha():
            errs.append("start with a letter")            
        if len(cbbox_val) < 3:
            errs.append("be at least three characters long")
        whitelist = string.ascii_letters + string.digits + '_'
        if not all(c in whitelist for c in cbbox_val):
            errs.append("contain only letters, digits, and underscores")
        if errs:
            message = "Username should:\n" + "\n".join(f"  - {err}" for err in errs)
            self.option_add("*Dialog.msg.font", self._small_font)
            self.option_add("*Dialog.msg.wrapLength", "0")
            messagebox.showinfo("Requirements", message)
            return
        
        self._user.create_user(cbbox_val)
        self._combobox['values'] = self._user.get_usernames()
        self._on_user_update()


    def _on_start_clicked(self):

        cbbox_val = self._combobox.get()
        
        self._user.load_user(cbbox_val)