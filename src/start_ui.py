
import tkinter as tk
from tkinter import ttk

from src.password_ui import PasswordUI
from src.settings_ui import SettingsUI
from src.frame_dict import FrameDict




class StartUI(tk.Tk):


    def __init__(self, user):

        super().__init__()
        self.user = user

        self.title("Math Facts")
        self.attributes('-type', 'dialog')
        
        self._main_button_text = tk.StringVar(value="Start")
        self._combobox_text = tk.StringVar(value="Select User")

        self._big_font = ("Arial", 42, "bold")
        self._little_font = ("Arial", 14)

        self._fd =  FrameDict(tk.Frame(self))
        self._make_layout()
        self._populate()
        self._fd.get('').pack(expand=True, fill="both")


    def _make_layout(self):

        self._fd.v_split('', [tk.Frame, tk.Frame], [3, 1])
        self._fd.h_split('v1', [tk.Frame, tk.Frame, tk.Frame], [12, 3, 1])


    def _populate(self):

        message = "Welcome to Math Facts!"
        self.title_label = tk.Label(
            self._fd.get('v0'), text=message, font=self._big_font)
        self.title_label.pack(fill='both', expand=True, padx=4, pady=4)
        
        self.user_combo = ttk.Combobox(
            self._fd.get('v1/h0'), values=self.user.get_usernames(), 
            state="normal", font=self._little_font, 
            textvariable=self._combobox_text)
        style = ttk.Style()
        style.configure("LeftPad.TCombobox", padding=(8, 0, 0, 0))
        self.user_combo.configure(style="LeftPad.TCombobox")
        self.user_combo.pack(fill='both', expand=True, padx=(4, 2), pady=4)
        self._combobox_text.trace_add('write', self._on_user_update)

        self.main_btn = tk.Button(
            self._fd.get('v1/h1'), textvariable=self._main_button_text,
            font=self._little_font, width=2, command=self._on_main_clicked)
        self.main_btn.pack(fill='both', expand=True, padx=(2, 2), pady=4)

        self.settings_btn = tk.Button(
            self._fd.get('v1/h2'), text="⚙", font=self._little_font,
            width=1, command=self._on_settings_clicked)
        self.settings_btn.pack(fill='both', padx=(2, 4), pady=4)

            
    def _on_start_clicked(self):

        cbbox_val = self._combobox_text.get()
        if cbbox_val == "Select User":
            return

        self.user.set_user(cbbox_val)


    def _on_create_clicked(self):

        cbbox_val = self._combobox_text.get().strip()
    
        errors = []
        criteria = lambda c: c.isalpha() or c.isdigit() or c == '_'
        if not all(criteria(c) for c in cbbox_val):
            errors.append("Username should contain only letters, digits,"
                          "or underscores.")
        if not cbbox_val:
            errors.append("Username should not be empty.")
        if len(cbbox_val) < 3:
            errors.append("Username should be at least three characters.")
        if not cbbox_val[0].isalpha():
            errors.append("Username should start with a letter.")

        if errors:
            err_message = "\n".join(errors)
            self._clear_error_popup()
            self._error_popup = tk.Toplevel(self)
            self._error_popup.overrideredirect(True)
            self._error_popup.configure(bg="lightyellow")
            label = tk.Label(
                self._error_popup, text=err_message, fg="red", 
                bg="lightyellow", font=("Arial", 12), justify="left")
            label.pack(padx=5, pady=5)
            x = self.user_combo.winfo_rootx()
            y = self.user_combo.winfo_rooty() - len(errors) * 30 - 17
            self._error_popup.geometry(f"+{x}+{y}")
            self.after(5000, self._clear_error_popup)
            return
        
        self.user.create_user(cbbox_val)
        self.user.set_user(cbbox_val)


    def _clear_error_popup(self):

        if hasattr(self, '_error_popup') and self._error_popup:
            self._error_popup.destroy()
            self._error_popup = None

 
    def _on_main_clicked(self):

        if self._main_button_text.get() == "Create":
            self._on_create_clicked()
            return
        elif self._main_button_text.get() == "Start":
            self._on_start_clicked()
            return


    def _on_settings_clicked(self):

        password_ui = 

    def _on_user_update(self, *args):

        user = self._combobox_text.get().strip()
        if not user:
            self._main_button_text.set("Start")
            return
        if user in UserData.get_usernames():
            self._main_button_text.set("Start")
        else:
            self._main_button_text.set("Create")