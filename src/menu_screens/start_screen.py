
import tkinter as tk



class StartScreen(tk.Frame):
    

    def __init__(self, mui):

        super().__init__(mui)

        self.mui = mui

        self._mui_frame = tk.Frame(mui)
        self._make_layout()

    
    def _make_layout(self):

        return