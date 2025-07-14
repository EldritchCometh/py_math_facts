
import tkinter as tk
from tkinter import ttk




class StartUI(tk.Tk):


    def __init__(self, app):
        
        super().__init__()

        self._start_button_text = "Start"

        self.app = app

        self.title("Math Facts")
        self.attributes('-type', 'dialog')

        self._frame = tk.Frame(self)
        self._make_layout()
        self._populate()
        self._frame.pack(expand=True, fill="both")

        self.user_var = tk.StringVar()
        self.user_var.trace_add('write', self._update_start_button)
    

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
        self.title_label = tk.Label(self.north_frame, text=message, font=("Arial", 42, "bold"))
        self.title_label.pack(anchor='center')
        
        font = ("Arial", 18)

        placeholder_users = ['user1', 'user2']
        self.user_combo = ttk.Combobox(self.south_frame, values=placeholder_users, state="normal", font=font)
        self.user_combo.pack(side='left', fill='both', expand=True, padx=4)

        self.start_btn = tk.Button(self.south_frame, text=self._start_button_text, font=font, width=1, command=self.change_start_button_text)
        self.start_btn.pack(side='left', fill='both', expand=True, padx=4)

        self.settings_btn = tk.Button(self.south_frame, text="⚙", font=font, width=1)
        self.settings_btn.pack(side='left', fill='y', padx=4)

    
    def _update_start_button(self, *args):
        
        user_input = self.user_var.get()
        if user_input:
            self.start_btn.config(state="normal")
        else:
            self.start_btn.config(state="disabled")
