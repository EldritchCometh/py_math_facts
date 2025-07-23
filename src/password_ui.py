
import tkinter as tk

from src.frame_dict import FrameDict



class PasswordUI(tk.Tk):


    def __init__(self, user):

        super().__init__()
        self.user = user

        self.title("Math Facts")
        self.attributes('-type', 'dialog')
        
        self._main_button_text = tk.StringVar(value="Start")
        self._combobox_text = tk.StringVar(value="Select User")

        self._big_font = ("Arial", 42, "bold")
        self._little_font = ("Arial", 14)

        self._fd =  FrameDict(tk.Frame(self))
        self._make_layout()
        self._populate()
        self._fd.get('').pack(expand=True, fill="both")