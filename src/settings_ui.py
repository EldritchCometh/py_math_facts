
import tkinter as tk
from tkinter import ttk

from src.user_data import UserData



class SettingsUI(tk.Tk):


    def __init__(self, app):

        super().__init__()
        
        self.app = app
        
        self.title("Settings")
        self.attributes('-type', 'dialog')
        
        self.ud = UserData()

        # Add settings UI components here
        label = ttk.Label(self, text="Settings will be implemented here.")
        label.pack(pady=20)
        
        # Example button to close settings
        close_button = ttk.Button(self, text="Close", command=self.destroy)
        close_button.pack(pady=10)
