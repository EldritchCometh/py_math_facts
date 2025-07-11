

import tkinter as tk



class MenuUI(tk.Tk):


    def __init__(self, app):
        
        super().__init__()

        self.app = app

        self.title("Math Facts")
        self.attributes('-type', 'dialog')

    
    def create_screen(self, screen_class):

        screen = screen_class(self)
        return screen
    

    def set_screen(self, screen):

        if self.screen is not None:
            self.screen._mui_frame.pack_forget()

        self.screen = screen
        self.screen._mui_frame.pack(expand=True, fill="both")
        self.screen.populate()