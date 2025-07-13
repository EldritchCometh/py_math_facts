
import tkinter as tk
from src.menu_screens.settings_screen import SettingsScreen


class StartScreen(tk.Frame):

    def __init__(self, mui):

        super().__init__(mui)

        self.mui = mui

        self._mui_frame = tk.Frame(mui)
        self._make_layout()

    
    def _make_layout(self):

        return
    
    
    def populate(self):

        return