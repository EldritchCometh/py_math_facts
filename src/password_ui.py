
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkfont
import string
import math
from pathlib import Path

from src.utils import *



class PasswordUI(tk.Toplevel):


    def __init__(self):

        super().__init__()
        
        self.title("Math Facts")
        self.attributes('-type', 'dialog')

        self._label_text = tk.StringVar()
        self._new_pass = ''
        self._verified = False

        self._pad = 4

        default_font = tkfont.nametofont("TkDefaultFont")
        self._big_font = tkfont.Font(
            family=default_font.actual()["family"], size=42, weight="bold")
        self._med_font = tkfont.Font(
            family=default_font.actual()["family"], size=14)
        self._small_font = tkfont.Font(
            family=default_font.actual()["family"], size=12)    

        style = ttk.Style(self)
        style.configure('TButton', font=self._small_font, padding=10)

        self.option_add("*Dialog.msg.font", self._small_font)
        self.option_add("*Dialog.msg.wrapLength", "40c")
        self.option_add("*Dialog.msg.wrap", "char")

        parent_dir = Path(__file__).resolve().parents[1]
        self._save_dir = Path.joinpath(parent_dir, 'data')
        self._pass_path = Path.joinpath(self._save_dir, f'passhash')
        
        self._default_passhash = sha256_hash('mathfacts')
        self._passhash = self._load_passhash()
        self._pass_set = not self._passhash == self._default_passhash

        self._new_pass = None

        self._main_frame = tk.Frame(self)
        self._make_layout(self._main_frame)
        self._main_frame.pack(expand=True, fill="both", padx=4, pady=4)
        

    def verify(self) -> bool:

        self.grab_set()
        self.wait_window()
        
        return self._verified
            

    def _load_passhash(self) -> str:

        try:
            with open(self._pass_path, 'r') as f:
                return f.read().strip()
        except: 
            raise FileNotFoundError("Password file missing.")


    def _make_layout(self, parent) -> None:

        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_rowconfigure(1, weight=1)
        parent.grid_rowconfigure(2, weight=1)

        self._title_label = None

        label_frame = tk.Frame(parent)
        entry_frame = tk.Frame(parent)
        button_frame = tk.Frame(parent)

        label_frame.grid(
            row=0, column=0, sticky='nsew', padx=self._pad, pady=self._pad)
        entry_frame.grid(
            row=1, column=0, sticky='nsew', padx=self._pad, pady=self._pad)
        button_frame.grid(
            row=2, column=0, sticky='nsew', padx=self._pad, pady=self._pad)

        self._label_frame(label_frame)
        self._entry_frame(entry_frame)
        self._button_frame(button_frame)


    def _label_frame(self, parent) -> None:

        frame = tk.Frame(parent)
        frame.pack(expand=True, fill='both', pady=self._pad)

        if self._pass_set:
            self._label_text.set("Enter Password:")
        else: 
            self._label_text.set("Create Password:")
        self._title_label = tk.Label(
            frame, textvariable=self._label_text, font=("Arial", 18))
        self._title_label.pack(side='left', padx=self._pad, pady=self._pad)


    def _entry_frame(self, parent) -> None:

        frame = tk.Frame(parent)
        frame.pack(expand=True, fill='both', padx=self._pad, pady=self._pad)

        self.password_entry = tk.Entry(frame, show='*', font=self._med_font)
        self.password_entry.pack(fill='both', expand=True, pady=self._pad)
        self.password_entry.focus_set()
        f = self._on_verify_clicked \
            if self._pass_set else self._on_create_clicked
        self.password_entry.bind('<Return>', lambda _: f())


    def _button_frame(self, parent) -> None:

        frame = tk.Frame(parent)
        frame.pack(expand=True, fill='both', pady=self._pad)
        
        text = "Verify" if self._pass_set else "Create"
        f = self._on_verify_clicked \
            if self._pass_set else self._on_create_clicked
        self._main_btn = ttk.Button(frame, text=text, style="TButton", command=f, width=10)
        self._cancel_btn = ttk.Button(frame, text="Cancel", style="TButton", command=self.destroy, width=10)
        
        self._main_btn.pack(side="right", fill='y', padx=self._pad)
        self._cancel_btn.pack(side="right", fill='y', padx=self._pad)
        
        
    def _on_verify_clicked(self) -> None:
        
        password = self.password_entry.get()
        if not password:
            return
        self.password_entry.delete(0, tk.END)
        
        hash_value = sha256_hash(password)
        
        if not hash_value == self._passhash:
            messagebox.showerror("Error", "Incorrect")
            self.password_entry.delete(0, tk.END)
            return
        
        self._verified = True
        self.destroy()


    def _on_create_clicked(self) -> None:
        
        password = self.password_entry.get()
        if not password:
            return
        self.password_entry.delete(0, tk.END)
        self.password_entry.focus_set()

        format_errs, strength_err = self._validate_password(password)
        if format_errs:
            message = "Password should:\n" 
            message += "\n".join(f"  - {err}" for err in format_errs)
            messagebox.showinfo("Format Warning", message)
            self.password_entry.delete(0, tk.END)
            return
        if strength_err and not self._new_pass:
            message = strength_err + (
                "\nWould you like to continue with this password anyway?")
            if not messagebox.askyesno("Weak Password", message):
                return

        if self._new_pass and password != self._new_pass:
            messagebox.showerror("Error", "Entries did not match.")
            self._new_pass = ''
            self.password_entry.delete(0, tk.END)
            self._label_text.set("Create Password:")
            return
        
        if not self._new_pass:
            self._new_pass = password
            self.password_entry.delete(0, tk.END)
            self._label_text.set("Retype Password:")
            return
        
        hash_value = sha256_hash(self._new_pass)
        with open(self._pass_path, 'w') as f:
            f.write(hash_value)
        
        self._verified = True
        self.destroy()

    
    def _validate_password(self, password) -> tuple[list[str], str]:

        format_errs = []
        if any(c.isspace() for c in password):
            format_errs.append("not contain whitespace")
        if len(password) < 6:
            format_errs.append("be at least six characters long")
        whitelist = \
            string.ascii_letters + string.digits + string.punctuation + '_'
        if not all(c in whitelist for c in password):
            format_errs.append("contain only letters, digits, underscores, \
                               and punctuation")      

        strength_err = ""
        err_msg = "This is a very weak password.\n"
        if not shannon_password_check(password):
            strength_err = err_msg
        if not basic_password_check(password):
            strength_err = err_msg
        
        return format_errs, strength_err
        

    

