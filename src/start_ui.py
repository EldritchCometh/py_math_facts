
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

    
    def change_start_button_text(self):
        print("this worked")
        self._start_button_text = "skibidi"
        

    def _make_layout(self):

        self._frame.columnconfigure(0, weight=1)
        self._frame.rowconfigure(0, weight=6)
        self._frame.rowconfigure(1, weight=1)

        self.north_frame = tk.Frame(self._frame)
        self.north_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=(2.5, 0))

        self.south_frame = tk.Frame(self._frame)
        self.south_frame.grid(row=1, column=0, sticky="nsew", padx=2.5, pady=5)


    def _populate(self):

        message = "Welcome to Math Facts!"
        self.title_label = tk.Label(self.north_frame, text=message, font=("Arial", 42, "bold"))
        self.title_label.pack(anchor='center')
        
        font = ("Arial", 22)

        placeholder_users = ['user1', 'user2']
        self.user_combo = ttk.Combobox(self.south_frame, values=placeholder_users, state="normal", font=font)
        self.user_combo.pack(side='left', fill='both', expand=True, padx=2.5)

        self.start_btn = tk.Button(self.south_frame, text=self._start_button_text, font=font, width=2, command=self.change_start_button_text)
        self.start_btn.pack(side='left', fill='both', expand=True, padx=2.5)
        
        self.settings_btn = tk.Button(self.south_frame, text="⚙", font=font, width=1)
        self.settings_btn.pack(side='left', fill='y', padx=2.5)



    # def create_screen(self, screen_class):

    #     screen = screen_class(self)
    #     return screen
    

    # def set_screen(self, screen):

    #     if self.screen is not None:
    #         self.screen._mui_frame.pack_forget()

    #     self.screen = screen
    #     self.screen._mui_frame.pack(expand=True, fill="both")
    #     self.screen.populate()