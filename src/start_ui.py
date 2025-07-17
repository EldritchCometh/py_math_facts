
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


    def _on_create_clicked(self):

        print("Create button clicked")
        return
    

    def _on_start_clicked(self):

        print("Start button clicked")
        return
    
    
    def _on_main_clicked(self):
        
        cbbox_val = self._combobox_text.get().strip()
        
        criteria = lambda c: c.isalpha() or c.isdigit() or c == '_'
        error_message = None
        if not cbbox_val or \
           not all(criteria(c) for c in cbbox_val) or \
           len(cbbox_val) < 3 or \
           not cbbox_val[0].isalpha():
            error_message = "Invalid username. Must be at least 3 characters long, \nstart with a letter, and contain only letters, \ndigits, or underscores."
            if hasattr(self, '_error_popup') and self._error_popup:
                self._error_popup.destroy()
            self._error_popup = tk.Toplevel(self)
            self._error_popup.overrideredirect(True)  # Borderless
            self._error_popup.configure(bg="lightyellow")
            label = tk.Label(self._error_popup, text=error_message, fg="red", bg="lightyellow", font=("Arial", 12))
            label.pack(padx=5, pady=5)
            # Position above combobox
            x = self.user_combo.winfo_rootx()
            y = self.user_combo.winfo_rooty() - 30  # Slightly above
            self._error_popup.geometry(f"+{x}+{y}")
            # Auto-hide after 3 seconds
            self.after(3000, self._clear_error_popup)
            return
        
        print(f"Main button clicked with user: {cbbox_val}")


    def _on_settings_clicked(self):

        print("Opening settings window")
        return


    def _on_user_update(self, *args):

        user = self._combobox_text.get().strip()
        if not user:
            self._main_button_text.set("Start")
            return
        if user in UserData.get_usernames():
            self._main_button_text.set("Start")
        else:
            self._main_button_text.set("Create")