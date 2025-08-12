
import tkinter as tk

from src.ready_screen import ReadyScreen
from src.play_screen import PlayScreen


class GameUI(tk.Toplevel):


    def __init__(self, app):
        
        super().__init__()
        self.app = app
        self.user = app.user
        self.facts = app.facts

        self.title("Math Facts")
        self.attributes('-type', 'dialog')

        screen_width = self.winfo_screenwidth()
        window_width = int(screen_width * 0.8)
        window_height = int(window_width * 0.25)
        self.geometry(f"{window_width}x{window_height}")

        self.after_ids = {}

        self.screen = None
        self.ready_screen = ReadyScreen(self)
        self.play_screen = PlayScreen(self)
        self.set_screen(self.ready_screen)


    def set_screen(self, screen) -> None:

        if self.screen is not None:
            self.screen._gui_frame.pack_forget()
        self.screen = screen

        screen._gui_frame.pack(expand=True, fill="both")
        self.update_idletasks()
        screen.resize()
        screen.populate()
        
        self._bind_with_debounce('<Configure>', lambda _: screen.resize())


    def _bind_with_debounce(self, event_type, func) -> None:

        def handler(event):
            if func.__name__ in self.after_ids:
                self.after_cancel(self.after_ids[func.__name__])
            self.after_ids[func.__name__] = self.after(100, lambda: func(event))

        self.bind(event_type, handler)