
import tkinter as tk
from tkinter import ttk

from src.user_data import UserData



class SettingsUI(tk.Toplevel):


    def __init__(self):

        super().__init__()
        
        self.title("Settings")
        self.attributes('-type', 'dialog')
        #self.geometry("600x400")

        self._padding = 2
        self._boarderwidth = 3
        self._font = ("Arial", 16)
        self.configure(padx=self._padding / 2, pady=self._padding / 2)

        self._frames = {}
        self._make_layout()
        self._populate()


    def _make_layout(self):

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)

        self._frames['numbers'] = tk.Frame(self, relief="raised", borderwidth=self._boarderwidth)
        self._frames['numbers'].grid(row=0, column=0, rowspan=5, sticky="nsew", padx=self._padding, pady=self._padding)

        self._frames['types'] = tk.Frame(self, relief="raised", borderwidth=self._boarderwidth)
        self._frames['types'].grid(row=0, column=1, rowspan=2, sticky="nsew", padx=self._padding, pady=self._padding)

        self._frames['patterns'] = tk.Frame(self, relief="raised", borderwidth=self._boarderwidth)
        self._frames['patterns'].grid(row=2, column=1, rowspan=1, sticky="nsew", padx=self._padding, pady=self._padding)

        self._frames['username'] = tk.Frame(self, relief="raised", borderwidth=self._boarderwidth)
        self._frames['username'].grid(row=3, column=1, rowspan=1, sticky="nsew", padx=self._padding, pady=self._padding)

        self._frames['timers'] = tk.Frame(self, relief="raised", borderwidth=self._boarderwidth)
        self._frames['timers'].grid(row=4, column=1, rowspan=1, sticky="nsew", padx=self._padding, pady=self._padding)

        self._frames['start_button'] = tk.Frame(self)
        self._frames['start_button'].grid(row=5, column=0, sticky="nsew", padx=self._padding, pady=self._padding)

        self._frames['cancel_button'] = tk.Frame(self)
        self._frames['cancel_button'].grid(row=5, column=1, sticky="nsew", padx=self._padding, pady=self._padding)


    def _populate_numbers_frame(self):

        numbers_frame = self._frames['numbers']

        numbers_frame.columnconfigure(0, weight=1)
        numbers_frame.columnconfigure(1, weight=1)
        for i in range(13):
            numbers_frame.rowconfigure(i, weight=1)
            var = tk.IntVar(value=1)
            check = tk.Checkbutton(numbers_frame, variable=var)
            check.grid(row=i, column=0, sticky="e")
            message = f"Include {i}"
            label = tk.Label(numbers_frame, text=message, font=self._font)
            label.grid(row=i, column=1, sticky="w", padx=(0, 6))


    def _populate_types_frame(self):

        types_frame = self._frames['types']

        types_frame.columnconfigure(0, weight=1)
        types_frame.columnconfigure(1, weight=1)
        for i in range(4):
            types_frame.rowconfigure(i, weight=1)
            var = tk.IntVar(value=1)
            check = tk.Checkbutton(types_frame, variable=var)
            check.grid(row=i, column=0, sticky="e")
            message = f"Type {i+1}"
            label = tk.Label(types_frame, text=message, font=self._font)
            label.grid(row=i, column=1, sticky="w")


    def _populate_patterns_frame(self):

        patterns_frame = self._frames['patterns']

        patterns_frame.columnconfigure(0, weight=1)
        patterns_frame.columnconfigure(1, weight=1)
        for i in range(2):
            patterns_frame.rowconfigure(i, weight=1)
            var = tk.IntVar(value=1)
            check = tk.Checkbutton(patterns_frame, variable=var)
            check.grid(row=i, column=0, sticky="e")
            message = f"Pattern {i+1}"
            label = tk.Label(patterns_frame, text=message, font=self._font)
            label.grid(row=i, column=1, sticky="w")


    def _populate_username_frame(self):

        username_frame = self._frames['username']
        username_frame.rowconfigure(0, weight=1)
        username_frame.rowconfigure(1, weight=1)
        
        label = tk.Label(username_frame, text="Change username:", font=self._font)
        label.grid(row=0, column=0, sticky="e", padx=4)

        entry = tk.Entry(username_frame, font=self._font, width=15)
        entry.grid(row=1, column=0, sticky="w", padx=4)

        # Here you would typically bind the entry to a variable or save it in UserData


    def _populate_timers_frame(self):

        timers_frame = self._frames['timers']
        timers_frame.rowconfigure(0, weight=1)
        timers_frame.rowconfigure(1, weight=1)

        label = tk.Label(timers_frame, text="Timer Values:", font=self._font)
        label.grid(row=0, column=0, sticky="w", padx=4)

        entry = tk.Entry(timers_frame, font=self._font, width=15)
        entry.grid(row=1, column=0, sticky="w", padx=4)

        # Here you would typically bind the entry to a variable or save it in UserData

        # Here you would typically add widgets for timer settings
        # For example, you could add entry fields for different timer values

    
    def _populate_buttons_frames(self):

        save_frame = self._frames['start_button']
        save_button = tk.Button(save_frame, text="Save", font=self._font, width=15, relief="raised", borderwidth=3, command=self._on_save_clicked)
        save_button.pack(expand=True, anchor='center')

        cancel_frame = self._frames['cancel_button']
        cancel_button = tk.Button(cancel_frame, text="Cancel", font=self._font, width=15, relief="raised", borderwidth=3, command=self._on_cancel_clicked)
        cancel_button.pack(expand=True, anchor='center')


    def _on_save_clicked(self):

        # Here you would implement the logic to save the settings
        # For example, you could save the state of checkboxes and entries to UserData
        print("Settings saved")
        self.destroy()

    
    def _on_cancel_clicked(self):

        # Here you would implement the logic to cancel the settings changes
        print("Settings changes canceled")
        self.destroy()


    def _populate(self):

        self._populate_numbers_frame()
        self._populate_types_frame()
        self._populate_patterns_frame()
        self._populate_username_frame()
        self._populate_timers_frame()
        self._populate_buttons_frames()