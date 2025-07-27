
import tkinter as tk
from tkinter import ttk
import copy
import tkinter.font as tkfont



class SettingsUI(tk.Toplevel):


    def __init__(self, user):

        super().__init__()
        
        self.user = user

        self.title("Math Facts Settings")
        self.attributes('-type', 'dialog')

        self._padding = 4
        self._boarderwidth = 4
        self._entry_widget_width = 10

        default_font = tkfont.nametofont("TkDefaultFont")
        self._big_font = tkfont.Font(family=default_font.actual()["family"], size=42, weight="bold")
        self._med_font = tkfont.Font(family=default_font.actual()["family"], size=14)
        self._small_font = tkfont.Font(family=default_font.actual()["family"], size=12)

        self._numbers = {}
        self._operators = {}
        self._patterns = {}
        self._timers = {}

        self._main_frame = tk.Frame(self)
        self._make_layout(self._main_frame)
        self._main_frame.pack(expand=True, fill="both", padx=self._padding, pady=self._padding)


    def _load_settings(self):

        user_settings = self.user.get_settings()

        self._numbers = copy.deepcopy(user_settings['numbers'])
        self._operators = copy.deepcopy(user_settings['operators'])
        self._patterns = copy.deepcopy(user_settings['patterns'])
        self._timers = copy.deepcopy(user_settings['timers'])


    def _save_settings(self):
        user_settings = {
            'numbers': self._numbers,
            'operators': self._operators,
            'patterns': self._patterns,
            'timers': self._timers }
        self.user.set_settings(user_settings)


    def _make_layout(self, parent):

        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_rowconfigure(1, weight=1)
        parent.grid_rowconfigure(2, weight=1)

        north_west_frame = tk.Frame(parent, bd=self._boarderwidth, relief="groove")
        north_east_frame = tk.Frame(parent)
        mid_west_frame = tk.Frame(parent, bd=self._boarderwidth, relief="groove")
        mid_east_frame = tk.Frame(parent, bd=self._boarderwidth, relief="groove")
        south_frame = tk.Frame(parent)

        north_west_frame.grid(row=0, column=0, sticky='nsew', padx=self._padding, pady=self._padding)
        north_east_frame.grid(row=0, column=1, sticky='nsew')
        mid_west_frame.grid(row=1, column=0, sticky='nsew', padx=self._padding, pady=self._padding)
        mid_east_frame.grid(row=1, column=1, sticky='nsew', padx=self._padding, pady=self._padding)
        south_frame.grid(row=2, column=0, columnspan=2, sticky='nsew', padx=self._padding, pady=self._padding)

        self._numbers_frame(north_west_frame)
        self._north_east_subdvide(north_east_frame)
        self._username_frame(mid_west_frame)
        self._password_frame(mid_east_frame)
        self._buttons_frame(south_frame)


    def _north_east_subdvide(self, parent):

        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_rowconfigure(1, weight=1)
        parent.grid_rowconfigure(2, weight=1)
        parent.grid_rowconfigure(3, weight=1)

        types_frame = tk.Frame(parent, bd=self._boarderwidth, relief="groove")
        patterns_frame = tk.Frame(parent, bd=self._boarderwidth, relief="groove")
        timers_frame = tk.Frame(parent, bd=self._boarderwidth, relief="groove")
        delete_frame = tk.Frame(parent, bd=self._boarderwidth, relief="groove")

        types_frame.grid(row=0, column=0, sticky='nsew', padx=self._padding, pady=self._padding)
        patterns_frame.grid(row=1, column=0, sticky='nsew', padx=self._padding, pady=self._padding)
        timers_frame.grid(row=2, column=0, sticky='nsew', padx=self._padding, pady=self._padding)
        delete_frame.grid(row=3, column=0, sticky='nsew', padx=self._padding, pady=self._padding)

        self._operators_frame(types_frame)
        self._patterns_frame(patterns_frame)
        self._timers_frame(timers_frame)
        self._delete_frame(delete_frame)


    def _numbers_frame(self, parent):
        
        frame = tk.Frame(parent)
        frame.pack(fill='both', expand=True, padx=4, pady=(4, 10))

        frame.grid_columnconfigure(0, weight=1)
        for i in range(14):
            frame.grid_rowconfigure(i, weight=1)

        label = tk.Label(frame, text="Include Numbers:", font=self._med_font)
        label.grid(row=0, column=0, sticky='w', padx=self._padding, pady=self._padding)

        for i in range(13):
            self._numbers[f'check_{i}'] = tk.BooleanVar(value=True)
            check = tk.Checkbutton(frame, text=f"Include {i}s", font=self._small_font, variable=var)
            check.grid(row=i+1, column=0, sticky='w')


    def _operators_frame(self, parent):
        
        frame = tk.Frame(parent)
        frame.pack(fill='both', expand=True, padx=self._padding, pady=(4, 10))

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_rowconfigure(2, weight=1)
        frame.grid_rowconfigure(3, weight=1)
        frame.grid_rowconfigure(4, weight=1)

        label = tk.Label(frame, text="Include Operators:", font=self._med_font)
        self._operators['main_label'] = {'widget': label}
        label.grid(row=0, column=0, sticky='w', padx=self._padding, pady=self._padding)

        names = ["Addition", "Subtraction", "Multiplication", "Division"]
        for i, opr in enumerate(names):
            var = tk.BooleanVar(value=True)
            check = tk.Checkbutton(frame, text=f"{opr}", font=self._small_font, variable=var)
            self._operators[f'check_{i}'] = {'var': var, 'widget': check}
            check.grid(row=i+1, column=0, sticky='w')


    def _patterns_frame(self, parent):

        frame = tk.Frame(parent)
        frame.pack(fill='both', expand=True, padx=self._padding, pady=(4, 10))

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_rowconfigure(2, weight=1)

        label = tk.Label(frame, text="Include Patterns:", font=self._med_font)
        self._patterns['main_label'] = {'widget': label}
        label.grid(row=0, column=0, sticky='w', padx=self._padding, pady=self._padding)

        names = ["Reversed", "Mixed Unknowns"]
        for i, opr in enumerate(names):
            var = tk.BooleanVar(value=True)
            check = tk.Checkbutton(frame, text=f"{opr}", font=self._small_font, variable=var)
            self._patterns[f'check_{i}'] = {'var': var, 'widget': check}
            check.grid(row=i+1, column=0, sticky='w')
        

    def _timers_frame(self, parent):

        frame = tk.Frame(parent)
        frame.pack(fill='both', expand=True, padx=self._padding, pady=self._padding)

        label = tk.Label(frame, text="Timers:", font=self._med_font)
        label.pack(anchor='nw', padx=self._padding, pady=self._padding)
        entry = tk.Entry(frame, font=self._med_font, width=self._entry_widget_width)
        entry.pack(fill='x', padx=self._padding, pady=self._padding)


    def _delete_frame(self, parent):

        frame = tk.Frame(parent)
        frame.pack(fill='both', expand=True, padx=self._padding, pady=self._padding)
        
        label = tk.Label(frame, text="Delete User:", font=self._med_font)
        label.pack(anchor='nw', padx=self._padding, pady=self._padding)
        
        style = ttk.Style()
        style.configure('TButton', font=self._small_font, padding=10)

        delete_button = ttk.Button(frame, text="Delete User", style='TButton', command=self._on_delete)
        delete_button.pack(fill='none', padx=self._padding, pady=self._padding)


    def _username_frame(self, parent):

        frame = tk.Frame(parent)
        frame.pack(fill='both', expand=True, padx=self._padding, pady=(4, 10))

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_rowconfigure(2, weight=1)

        main_label = tk.Label(frame, text="Change Username:", font=self._med_font)
        current_label = tk.Label(frame, text="Current:", font=self._small_font)
        current_entry = tk.Entry(frame, font=self._small_font, width=self._entry_widget_width)
        new_label = tk.Label(frame, text="New:", font=self._small_font)
        new_entry = tk.Entry(frame, font=self._small_font, width=self._entry_widget_width)

        main_label.grid(row=0, column=0, columnspan=2, sticky='w', padx=self._padding, pady=self._padding)
        current_label.grid(row=1, column=0, sticky='w', padx=(16, 4))
        current_entry.grid(row=1, column=1, sticky='w', padx=(4, 8))
        new_label.grid(row=2, column=0, sticky='w', padx=(16, 4))
        new_entry.grid(row=2, column=1, sticky='w', padx=(4, 8))


    def _password_frame(self, parent):

        frame = tk.Frame(parent)
        frame.pack(fill='both', expand=True, padx=4, pady=(4, 10))

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_rowconfigure(2, weight=1)

        main_label = tk.Label(frame, text="Change Password:", font=self._med_font)
        current_label = tk.Label(frame, text="Current:", font=self._small_font)
        current_entry = tk.Entry(frame, font=self._small_font, width=self._entry_widget_width)
        new_label = tk.Label(frame, text="New:", font=self._small_font)
        new_entry = tk.Entry(frame, font=self._small_font, width=self._entry_widget_width)

        main_label.grid(row=0, column=0, columnspan=2, sticky='w', padx=self._padding, pady=self._padding)
        current_label.grid(row=1, column=0, sticky='w', padx=(16, 4))
        current_entry.grid(row=1, column=1, sticky='w', padx=(4, 8))
        new_label.grid(row=2, column=0, sticky='w', padx=(16, 4))
        new_entry.grid(row=2, column=1, sticky='w', padx=(4, 8))


    def _buttons_frame(self, parent):
        
        frame = tk.Frame(parent)
        frame.pack(fill='x', side='bottom', padx=self._padding, pady=self._padding)

        style = ttk.Style()
        style.configure('TButton', font=self._med_font, padding=10)

        save_button = ttk.Button(frame, text="Save", style='TButton', command=self._on_save, width=10)
        cancel_button = ttk.Button(frame, text="Cancel", style='TButton', command=self._on_cancel, width=10)
        save_button.pack(side="right", padx=(10, 0))
        cancel_button.pack(side="right", padx=10)


    def _on_delete(self):

        return


    def _on_save(self):

        return
    

    def _on_cancel(self):

        self.destroy()