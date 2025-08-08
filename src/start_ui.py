
import string
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as tkfont

from src.password_ui import PasswordUI
from src.options_ui import OptionsUI



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
        
        style = ttk.Style()
        style.configure('TButton', font=self._small_font, padding=10)

        self.option_add("*Dialog.msg.font", self._small_font)
        self.option_add("*Dialog.msg.wrapLength", "40c")
        self.option_add("*Dialog.msg.wrap", "char")

        self._combobox: ttk.Combobox
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

        self._combobox = ttk.Combobox(
            frame, values=self._user.get_saved_users(), state="normal", 
            font=self._small_font, textvariable=self._combobox_text)
        create_btn = ttk.Button(frame, text="Create", style='TButton', command=self._on_create_clicked, width=10)
        start_btn = ttk.Button(frame, text="Start", style='TButton', command=self._on_start_clicked, width=10)
        options_btn = ttk.Button(frame, text="⚙", style='TButton', command=self._on_options_clicked, width=3)
        

        options_btn.pack(side='right', fill='y', padx=self._padding)
        start_btn.pack(side='right', fill='y', padx=self._padding)
        create_btn.pack(side='right', fill='y', padx=self._padding)
        self._combobox.pack(side='right', fill='y', padx=self._padding)


    def _on_start_clicked(self):

        cbbox_val = self._combobox.get()
        if cbbox_val in self._user.get_saved_users():
                self._user.load_saved_user(cbbox_val)
        else:
            return
        
        self.destroy()

    
    def _on_create_clicked(self):

        cbbox_val = self._combobox.get()
        if not cbbox_val.strip():
            return
        if cbbox_val.strip() == "Select User":
            return
        if cbbox_val in self._user.get_saved_users():
            return
        
        errs = []
        if not cbbox_val[0].isalpha():
            errs.append("begin with a letter")
        if not any(c in string.ascii_letters for c in cbbox_val):
            errs.append("contain at least one letter")
        if any(c.isspace() for c in cbbox_val):
            errs.append("not contain whitespace")
        if len(cbbox_val) < 2:
            errs.append("be at least two characters long")
        whitelist = string.ascii_letters + string.digits + '_'
        if not all(c in whitelist for c in cbbox_val):
            errs.append("contain only letters, digits or underscores")
        if errs:
            message = "Username should:\n" + "\n".join(f"  - {err}" for err in errs)
            messagebox.showinfo("Requirements", message)
            return
        
        if PasswordUI().verify():
            self._user.create_user(cbbox_val)
            self._combobox['values'] = self._user.get_saved_users()


    def _on_options_clicked(self):

        cbbox_val = self._combobox.get()
        if cbbox_val in self._user.get_saved_users():
                self._user.load_saved_user(cbbox_val)
        else:
            return

        if PasswordUI().verify():
            options_ui = OptionsUI(self._user)
            self.wait_window(options_ui)
        
        self._combobox['values'] = self._user.get_saved_users()
        self._combobox.set("Select User")