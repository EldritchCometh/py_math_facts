
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkfont
import string

from src.password_ui import PasswordUI
from src.options_ui import OptionsUI



class StartUI(tk.Toplevel):


    def __init__(self, app):

        super().__init__()
        self._app = app
        self._user = app.user

        self.title("Start UI")
        self.attributes('-type', 'dialog')
        self.protocol("WM_DELETE_WINDOW", app.destroy)

        self._pad = 4
        self._borderwidth = 3

        default_font = tkfont.nametofont("TkDefaultFont")
        self._big_font = tkfont.Font(
            family=default_font.actual()["family"], size=42, weight="bold")
        self._med_font = tkfont.Font(
            family=default_font.actual()["family"], size=14)
        self._small_font = tkfont.Font(
            family=default_font.actual()["family"], size=12)
        
        style = ttk.Style()
        style.configure('TButton', font=self._small_font, padding=10)
        style.configure(
            'TCombobox', font=self._small_font, 
            padding=[12, 0, 0, 0], arrowsize=24)

        self.option_add("*Dialog.msg.font", self._small_font)
        self.option_add("*Dialog.msg.wrapLength", "40c")
        self.option_add("*Dialog.msg.wrap", "char")

        self._combobox: ttk.Combobox
        self._combobox_text = tk.StringVar(value="Select User")

        self._main_frame = tk.Frame(self)
        self._make_layout(self._main_frame)
        self._main_frame.pack(expand=True, fill='both', padx=4, pady=4)


    def _make_layout(self, parent) -> None:

        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_rowconfigure(1, weight=1)

        welcome_frame = tk.Frame(parent, bd=self._borderwidth, relief="groove")
        widgets_frame = tk.Frame(parent)

        welcome_frame.grid(
            row=0, column=0, sticky='nsew', padx=self._pad, pady=self._pad)
        widgets_frame.grid(
            row=1, column=0, sticky='nsew', padx=self._pad, pady=self._pad)

        self._welcome_frame(welcome_frame)
        self._widgets_frame(widgets_frame)


    def _welcome_frame(self, parent) -> None:

        frame = tk.Frame(parent)
        frame.pack(expand=True, fill='both')

        message = "Welcome to Math Facts!"
        title_label = tk.Label(frame, text=message, font=self._big_font)
        title_label.pack(fill='both', expand=True, padx=18, pady=self._pad)


    def _widgets_frame(self, parent) -> None:

        frame = tk.Frame(parent)
        frame.pack(expand=True, fill='both', pady=self._pad)

        self._combobox = ttk.Combobox(
            frame, values=self._user.get_saved_users(), state="normal", 
            font=self._small_font, textvariable=self._combobox_text)
        create_btn = ttk.Button(
            frame, text="Create", style='TButton', 
            command=self._on_create_clicked, width=10)
        start_btn = ttk.Button(
            frame, text="Start", style='TButton', 
            command=self._on_start_clicked, width=10)
        options_btn = ttk.Button(
            frame, text="⚙", style='TButton', 
            command=self._on_options_clicked, width=3)
        
        options_btn.pack(side='right', fill='y', padx=self._pad)
        start_btn.pack(side='right', fill='y', padx=self._pad)
        create_btn.pack(side='right', fill='y', padx=self._pad)
        self._combobox.pack(side='right', fill='y', padx=self._pad)
        self._combobox.bind(
            "<ButtonRelease-1>", 
            lambda _: self._combobox.select_range(0, tk.END))


    def _on_start_clicked(self) -> None:

        cbbox_val = self._combobox.get()
        if cbbox_val in self._user.get_saved_users():
                self._user.load_saved_user(cbbox_val)
        else:
            return
        
        self._app.on_start_clicked()

    
    def _on_create_clicked(self) -> None:

        cbbox_val = self._combobox.get()
        
        valid, errs = self._validate_username(cbbox_val)
        if errs:
            message = "Username should:\n" 
            message += "\n".join(f"  - {err}" for err in errs)
            messagebox.showinfo("Requirements", message)
            return
        if not valid:
            return

        if PasswordUI().verify():
            self._user.create_new_user(cbbox_val)
            self._combobox['values'] = self._user.get_saved_users()


    def _on_options_clicked(self) -> None:

        cbbox_val = self._combobox.get()
        if cbbox_val in self._user.get_saved_users():
                self._user.load_saved_user(cbbox_val)
        else:
            return

        if PasswordUI().verify():
            options_ui = OptionsUI(self._user)
            self.wait_window(options_ui)
    
        self._combobox['values'] = self._user.get_saved_users()
        self._combobox_text.set("Select User")
        self._combobox.select_range(0, tk.END)


    def _validate_username(self, cbbox_val: str) -> tuple[bool, list[str]]:

        if not cbbox_val.strip():
            return False, ["Username cannot be empty"]
        if cbbox_val.strip() == "Select User":
            return False, []
        if cbbox_val in self._user.get_saved_users():
            return False, []

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
            return False, errs
        else:
            return True, []
