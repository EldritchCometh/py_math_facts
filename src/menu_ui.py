
import tkinter as tk
from .menu_screens.start_screen import StartScreen
from .menu_screens.settings_screen import SettingsScreen



class MenuUI(tk.Tk):


    def __init__(self, app):
        
        super().__init__()

        self.app = app

        self.title("Math Facts")
        self.attributes('-type', 'dialog')

        start_screen = self.create_screen(StartScreen)

    
    def create_screen(self, screen_class):

        screen = screen_class(self)
        return screen
    

    def set_screen(self, screen):

        if self.screen is not None:
            self.screen._mui_frame.pack_forget()

        self.screen = screen
        self.screen._mui_frame.pack(expand=True, fill="both")
        self.screen.populate()