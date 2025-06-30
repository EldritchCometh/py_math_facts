
import tkinter as tk
from src.screens.play_screen import PlayScreen



class MathFactsUI(tk.Tk):


    def __init__(self, app):
        
        super().__init__()
        
        self.app = app

        self.title("Math Facts")
        self.attributes('-type', 'dialog')

        screen_width = self.winfo_screenwidth()
        window_width = int(screen_width * 0.8)
        window_height = int(window_width * 0.25)
        self.geometry(f"{window_width}x{window_height}")

        self.screen = None
        self.play_screen = PlayScreen(self)


    def set_screen_play(self):
        
        if self.screen is not None:
            self.screen._ui_frame.pack_forget()

        self.screen = self.play_screen
        self.update_idletasks()
        self.screen.populate()
        self.screen.resize(self.winfo_width(), self.winfo_height())
        self.screen._ui_frame.pack(expand=True, fill="both")
