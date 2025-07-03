
import tkinter as tk
from src.screens.play_screen import PlayScreen
from src.screens.start_screen import StartScreen



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

        self.after_ids = {}

        self.screen = None
        self.play_screen = PlayScreen(self)
        self.start_screen = StartScreen(self)


    def set_screen_start(self):

        if self.screen is not None:
            self.screen._ui_frame.pack_forget()

        self.screen = self.start_screen
        self.update_idletasks()
        self.screen.populate()
        self.screen.resize(self.winfo_width, self.winfo_height)
        resize = lambda _: \
            self.screen.resize(self.winfo_width, self.winfo_height)
        self._bind_with_debounce('<Configure>', resize)
        self.screen._ui_frame.pack(expand=True, fill="both")


    def set_screen_play(self):
        
        if self.screen is not None:
            self.screen._ui_frame.pack_forget()

        self.screen = self.play_screen
        self.update_idletasks()
        self.screen.populate()
        self.screen.resize(self.winfo_width, self.winfo_height)
        resize = lambda _: \
            self.screen.resize(self.winfo_width, self.winfo_height)
        self._bind_with_debounce('<Configure>', resize)
        self.screen._ui_frame.pack(expand=True, fill="both")


    def _bind_with_debounce(self, event_type, func):

        def handler(event):
            if func.__name__ in self.after_ids:
                self.after_cancel(self.after_ids[func.__name__])
            self.after_ids[func.__name__] = \
                self.after(100, lambda: func(event))
            
        self.bind(event_type, handler)