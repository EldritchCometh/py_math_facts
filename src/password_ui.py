
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from pathlib import Path
import hashlib
import string
import tkinter.font as tkfont

from src.settings_ui import SettingsUI



class PasswordUI(tk.Toplevel):


    def __init__(self, user):

        super().__init__()
        
        self.user = user
        
        self.title("Math Facts")
        self.attributes('-type', 'dialog')

        self._padding = 4

        default_font = tkfont.nametofont("TkDefaultFont")
        self._big_font = tkfont.Font(family=default_font.actual()["family"], size=42, weight="bold")
        self._med_font = tkfont.Font(family=default_font.actual()["family"], size=14)
        self._small_font = tkfont.Font(family=default_font.actual()["family"], size=12)    

        parent_dir = Path(__file__).resolve().parents[1]
        self.save_dir = Path.joinpath(parent_dir, 'app_data')
        self._pass_path = Path.joinpath(self.save_dir, f'passhash')
        self._pass_exists = self._pass_path.exists()

        self._main_btn: ttk.Button
        
        self._main_frame = tk.Frame(self)
        self._make_layout(self._main_frame)
        self._main_frame.pack(expand=True, fill="both", padx=4, pady=4)
        

    def _make_layout(self, parent):

        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_rowconfigure(1, weight=1)
        parent.grid_rowconfigure(2, weight=1)

        label_frame = tk.Frame(parent)
        entry_frame = tk.Frame(parent)
        button_frame = tk.Frame(parent)

        label_frame.grid(row=0, column=0, sticky='nsew', padx=self._padding, pady=self._padding)
        entry_frame.grid(row=1, column=0, sticky='nsew', padx=self._padding, pady=self._padding)
        button_frame.grid(row=2, column=0, sticky='nsew', padx=self._padding, pady=self._padding)

        self._label_frame(label_frame)
        self._entry_frame(entry_frame)
        self._button_frame(button_frame)


    def _label_frame(self, parent):

        frame = tk.Frame(parent)
        frame.pack(expand=True, fill='both', pady=self._padding)

        text = "Enter Password:" if self._pass_exists else "Create Password:"
        self.title_label = tk.Label(
            frame, text=text, font=("Arial", 18))
        self.title_label.pack(side='left', padx=self._padding, pady=self._padding)


    def _entry_frame(self, parent):

        frame = tk.Frame(parent)
        frame.pack(expand=True, fill='both', padx=self._padding, pady=self._padding)

        self.password_entry = tk.Entry(frame, show='*', font=self._med_font)
        self.password_entry.pack(fill='both', expand=True, pady=self._padding)


    def _button_frame(self, parent):

        frame = tk.Frame(parent)
        frame.pack(expand=True, fill='both', pady=self._padding)

        style = ttk.Style(self)
        style.configure('TButton', font=self._med_font, padding=10)
        
        text = "Verify" if self._pass_exists else "Create"
        f = self._on_verify_clicked if self._pass_exists else self._on_create_clicked
        self._main_btn = ttk.Button(frame, text=text, style="TButton", command=f, width=10)
     
        self._main_btn.pack(side="right", fill='y', padx=self._padding)
       

    def _on_verify_clicked(self):
        
        # password = self.password_entry.get()
        # self.password_entry.delete(0, tk.END)
        # if not password:
        #     return
        
        # hash_value = hashlib.sha256(password.encode('utf-8')).hexdigest()
        # with open(self._pass_path, 'r') as f:
        #     stored_hash = f.read().strip()
        
        # if hash_value != stored_hash:
        #     messagebox.showerror("Error", "Incorrect")
        #     return
        
        SettingsUI(self.user)
        self.destroy()


    def _on_create_clicked(self):
        
        password = self.password_entry.get()
        if not password:
            return
        self.password_entry.delete(0, tk.END)
        
        errs = []
        if any(c.isspace() for c in password):
            errs.append("not contain whitespace")
        if len(password) < 4:
            errs.append("be at least four characters long")
        whitelist = string.ascii_letters + string.digits + string.punctuation + '_'
        if not all(c in whitelist for c in password):
            errs.append("contain only letters, digits, underscores, and punctuation")
        if errs:
            message = "Username should:\n" + "\n".join(f"  - {err}" for err in errs)
            self.option_add("*Dialog.msg.font", self._small_font)
            self.option_add("*Dialog.msg.wrapLength", "0")
            messagebox.showinfo("Requirements", message)
            self.password_entry.delete(0, tk.END)
            return

        self.save_dir.mkdir(parents=True, exist_ok=True)
        hash_value = hashlib.sha256(password.encode('utf-8')).hexdigest()
        with open(self._pass_path, 'w') as f:
            f.write(hash_value)
        self._pass_exists = True
        self.title_label.config(text="Enter Password:")
        self._main_btn.config(text="Submit", command=self._on_verify_clicked)