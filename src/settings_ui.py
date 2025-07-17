
import tkinter as tk
from tkinter import ttk

from src.user_data import UserData



class SettingsUI(tk.Tk):


    def __init__(self):

        super().__init__()
        
        self.title("Settings")
        self.attributes('-type', 'dialog')
        self.geometry("600x400")
        
        self._frames = {}
        self._make_layout()
        self._populate()


    def _make_layout(self):

        # Included numbers    - 13 checkboxes
        # Included fact types -  4 checkboxes
        # Included patterns   -  2 checkboxes
        # Change username - entry field - button
        # Timers - entry field
        # Save button - Cancel button

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)

        self._frames['numbers'] = tk.Frame(self, bg="#e0f7fa")
        self._frames['numbers'].grid(row=0, column=0, rowspan=6, sticky="nsew")

        self._frames['types'] = tk.Frame(self, bg="#ffe0b2")
        self._frames['types'].grid(row=0, column=1, rowspan=2, sticky="nsew")

        self._frames['patterns'] = tk.Frame(self, bg="#c8e6c9")
        self._frames['patterns'].grid(row=2, column=1, rowspan=1, sticky="nsew")

        self._frames['username'] = tk.Frame(self, bg="#f8bbd0")
        self._frames['username'].grid(row=3, column=1, rowspan=3, sticky="nsew")


    def _populate(self):

        return