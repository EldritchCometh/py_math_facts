
import tkinter as tk
from tkinter import ttk

from src.user_data import UserData
from src.settings_ui import SettingsUI




class StartUI(tk.Tk):


    def __init__(self, user):

        super().__init__()
        self.user = user

        self.title("Math Facts")
        self.attributes('-type', 'dialog')
        
        self._main_button_text = tk.StringVar(value="Start")
        self._combobox_text = tk.StringVar(value="Select User")

        self._frame = tk.Frame(self)
        self._make_layout()
        self._populate()
        self._frame.pack(expand=True, fill="both")


    def _make_layout(self):

        self._frame.columnconfigure(0, weight=1)
        self._frame.rowconfigure(0, weight=6)
        self._frame.rowconfigure(1, weight=1)

        self.north_frame = tk.Frame(self._frame)
        self.north_frame.grid(row=0, column=0, sticky="nsew", padx=16, pady=(6, 2))

        self.south_frame = tk.Frame(self._frame)
        self.south_frame.grid(row=1, column=0, sticky="nsew", padx=4, pady=8)


    def _populate(self):

        message = "Welcome to Math Facts!"
        self.title_label = tk.Label(
            self.north_frame, text=message, font=("Arial", 42, "bold"))
        self.title_label.pack(anchor='center')
        
        font = ("Arial", 18)

        self.user_combo = ttk.Combobox(
            self.south_frame, values=UserData.get_usernames(), 
            state="normal", font=font, textvariable=self._combobox_text)
        self.user_combo.pack(side='left', fill='both', expand=True, padx=4)
        self._combobox_text.trace_add('write', self._on_user_update)

        self.main_btn = tk.Button(
            self.south_frame, textvariable=self._main_button_text,
            font=font, width=2, command=self._on_main_clicked)
        self.main_btn.pack(side='left', fill='both', expand=True, padx=4)

        self.settings_btn = tk.Button(
            self.south_frame, text="⚙", font=font, 
            width=1, command=self._on_settings_clicked)
        self.settings_btn.pack(side='left', fill='y', padx=4)

            
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

        settings_ui = SettingsUI()
        settings_ui.mainloop()


    def _on_user_update(self, *args):

        user = self._combobox_text.get().strip()
        if not user:
            self._main_button_text.set("Start")
            return
        if user in UserData.get_usernames():
            self._main_button_text.set("Start")
        else:
            self._main_button_text.set("Create")