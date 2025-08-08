
import base64
import math
import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from pathlib import Path
import hashlib
import string
import tkinter.font as tkfont

from src.options_ui import OptionsUI
from src.utils.common_passhashes import common_passhashes



class PasswordUI(tk.Toplevel):


    def __init__(self):

        super().__init__()
        
        self.title("Math Facts")
        self.attributes('-type', 'dialog')

        self._label_text = tk.StringVar()
        self._new_pass = ''
        self._verified = False

        self._padding = 4

        default_font = tkfont.nametofont("TkDefaultFont")
        self._big_font = tkfont.Font(family=default_font.actual()["family"], size=42, weight="bold")
        self._med_font = tkfont.Font(family=default_font.actual()["family"], size=14)
        self._small_font = tkfont.Font(family=default_font.actual()["family"], size=12)    

        style = ttk.Style(self)
        style.configure('TButton', font=self._small_font, padding=10)

        self.option_add("*Dialog.msg.font", self._small_font)
        self.option_add("*Dialog.msg.wrapLength", "40c")
        self.option_add("*Dialog.msg.wrap", "char")

        parent_dir = Path(__file__).resolve().parents[1]
        self.save_dir = Path.joinpath(parent_dir, 'app_data')
        self._pass_path = Path.joinpath(self.save_dir, f'passhash')
        self._pass_exists = self._pass_path.exists()
        
        self._main_frame = tk.Frame(self)
        self._make_layout(self._main_frame)
        self._main_frame.pack(expand=True, fill="both", padx=4, pady=4)
        

    def verify(self):

        self.grab_set()
        self.wait_window()
        
        return self._verified


    def _make_layout(self, parent):

        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_rowconfigure(1, weight=1)
        parent.grid_rowconfigure(2, weight=1)

        self._title_label = None

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

        if self._pass_exists:
            self._label_text.set("Enter Password:")
        else: 
            self._label_text.set("Create Password:")
        self._title_label = tk.Label(frame, textvariable=self._label_text, font=("Arial", 18))
        self._title_label.pack(side='left', padx=self._padding, pady=self._padding)


    def _entry_frame(self, parent):

        frame = tk.Frame(parent)
        frame.pack(expand=True, fill='both', padx=self._padding, pady=self._padding)

        self.password_entry = tk.Entry(frame, show='*', font=self._med_font)
        self.password_entry.pack(fill='both', expand=True, pady=self._padding)


    def _button_frame(self, parent):

        frame = tk.Frame(parent)
        frame.pack(expand=True, fill='both', pady=self._padding)
        
        text = "Verify" if self._pass_exists else "Create"
        f = self._on_verify_clicked if self._pass_exists else self._on_create_clicked
        self._main_btn = ttk.Button(frame, text=text, style="TButton", command=f, width=10)
     
        self._main_btn.pack(side="right", fill='y', padx=self._padding)
       

    def _on_verify_clicked(self):
        
        # password = self.password_entry.get()
        # if not password:
        #     return
        # self.password_entry.delete(0, tk.END)
        
        # hash_value = hashlib.sha256(password.encode('utf-8')).hexdigest()
        
        # try:
        #     with open(self._pass_path, 'r') as f:
        #         stored_hash = f.read().strip()
        # except (OSError, IOError) as e:
        #     messagebox.showerror("Error", f"Failed to read password file: {e}")
        #     return
        
        # if hash_value != stored_hash:
        #     messagebox.showerror("Error", "Incorrect")
        #     self.password_entry.delete(0, tk.END)
        #     return
        
        self._verified = True
        self.destroy()


    def _on_create_clicked(self):
        
        password = self.password_entry.get()
        if not password:
            return
        self.password_entry.delete(0, tk.END)

        if self._new_pass and password != self._new_pass:
            messagebox.showerror("Error", "Entries did not match.")
            self._new_pass = ''
            self.password_entry.delete(0, tk.END)
            self._label_text.set("Create Password:")
            return

        errs = []
        if any(c.isspace() for c in password):
            errs.append("not contain whitespace")
        if len(password) < 4:
            errs.append("be at least four characters long")
        whitelist = string.ascii_letters + string.digits + string.punctuation + '_'
        if not all(c in whitelist for c in password):
            errs.append("contain only letters, digits, underscores, and punctuation")      
        if errs:
            message = "Password should:\n" + "\n".join(f"  - {err}" for err in errs)
            messagebox.showinfo("Requirements", message)
            self.password_entry.delete(0, tk.END)
            return
        
        err = ''
        if PasswordUI._hash(password) in common_passhashes:
            err = "This is a very common password.\n"
        elif not self.shannon_password_check(password):
            err = "This is a very weak password.\n"
        if err:
            err += (
                "\nTips for a strong, memorable password:\n"
                "- Use camel-cased, alliterative nonsense words.\n"
                "- Add a short, meaningful number sequence.\n"
                "- Include one punctuation mark.\n"
                "- Examples: 'MeanMrMustard42!', 'LizardLordLargess@67'"
            )
            messagebox.showwarning("Weak Password Warning", err)
            return
        
        if not self._new_pass:
            self._new_pass = password
            self.password_entry.delete(0, tk.END)
            self._label_text.set("Retype New Password:")
            return
        
        try:
            self.save_dir.mkdir(parents=True, exist_ok=True)
            hash_value = hashlib.sha256(password.encode('utf-8')).hexdigest()
            with open(self._pass_path, 'w') as f:
                f.write(hash_value)
        except (OSError, IOError) as e:
            messagebox.showerror("Error", f"Failed to save password: {e}")
            return
        
        self._verified = True
        self.destroy()

    @staticmethod
    def _hash(password):
        
        encoded = password.encode()
        sha_256 = hashlib.sha256(encoded).digest()
        base_64 = base64.b64encode(sha_256).decode()
        return base_64[:6]


    @staticmethod
    def shannon_password_check(password):
        
        if not password:
            return False
        char_count = len(password)
        freq = {}
        for char in password:
            freq[char] = freq.get(char, 0) + 1
        entropy_per_char = 0
        for count in freq.values():
            prob = count / char_count
            entropy_per_char -= prob * math.log2(prob)
        total_entropy = entropy_per_char * char_count
        return total_entropy > 20
    