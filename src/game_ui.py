
import tkinter as tk
from .game_screens.play_screen import PlayScreen
from .game_screens.ready_screen import ReadyScreen



class GameUI(tk.Tk):


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
        self.ready_screen = self.create_screen(ReadyScreen)
        self.play_screen = self.create_screen(PlayScreen)
        self.set_screen(self.ready_screen)


    def create_screen(self, screen_class):

        screen = screen_class(self)
        return screen


    def set_screen(self, screen):

        if self.screen is not None:
            self.screen._ui_frame.pack_forget()

        self.screen = screen
        self.screen._ui_frame.pack(expand=True, fill="both")
        self.update_idletasks()
        self.screen.resize()
        self.screen.populate()
        self._bind_with_debounce('<Configure>', lambda _: screen.resize())
        


    def _bind_with_debounce(self, event_type, func):

        def handler(event):
            if func.__name__ in self.after_ids:
                self.after_cancel(self.after_ids[func.__name__])
            self.after_ids[func.__name__] = self.after(100, lambda: func(event))

        self.bind(event_type, handler)