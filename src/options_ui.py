
import base64
import os
import tkinter as tk
from tkinter import ttk
from copy import deepcopy as copy
from tkinter import messagebox
import tkinter.font as tkfont
import hashlib
from pathlib import Path



class OptionsUI(tk.Toplevel):


    def __init__(self, user):

        super().__init__()
        
        self._user = user

        self.title("Math Facts Settings")
        self.attributes('-type', 'dialog')

        self._padding = 4
        self._boarderwidth = 4
        self._entry_widget_width = 10

        default_font = tkfont.nametofont("TkDefaultFont")
        self._big_font = tkfont.Font(family=default_font.actual()["family"], size=42, weight="bold")
        self._med_font = tkfont.Font(family=default_font.actual()["family"], size=14)
        self._small_font = tkfont.Font(family=default_font.actual()["family"], size=12)

        self.option_add("*Dialog.msg.font", self._small_font)
        self.option_add("*Dialog.msg.wrapLength", "40c")
        self.option_add("*Dialog.msg.wrap", "char")

        style = ttk.Style()
        style.configure('TButton', font=self._small_font, padding=10)

        self._inc_nums: dict = {}
        self._inc_oprs: dict = {}
        self._inc_ptrns: dict = {}
        self._num_facts = tk.StringVar()
        self._inc_timers = tk.BooleanVar()
        self._inc_untimed = tk.BooleanVar()
        self._timers = tk.StringVar()
        self._new_username = tk.StringVar()
        self._new_password = tk.StringVar()
        self._load_settings()

        self._main_frame = tk.Frame(self)
        self._make_layout(self._main_frame)
        self._main_frame.pack(expand=True, fill="both", padx=self._padding, pady=self._padding)


    def _make_layout(self, parent):

        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        parent.grid_columnconfigure(2, weight=1)
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_rowconfigure(1, weight=1)
        parent.grid_rowconfigure(2, weight=1)
        parent.grid_rowconfigure(3, weight=1)
        parent.grid_rowconfigure(4, weight=1)

        inc_nums = tk.Frame(parent, bd=self._boarderwidth, relief="groove")
        inc_oprs = tk.Frame(parent, bd=self._boarderwidth, relief="groove")
        inc_ptrns = tk.Frame(parent, bd=self._boarderwidth, relief="groove")
        timers = tk.Frame(parent, bd=self._boarderwidth, relief="groove")
        username = tk.Frame(parent, bd=self._boarderwidth, relief="groove")
        delete = tk.Frame(parent, bd=self._boarderwidth, relief="groove")
        password = tk.Frame(parent, bd=self._boarderwidth, relief="groove")
        num_facts = tk.Frame(parent, bd=self._boarderwidth, relief="groove")
        buttons = tk.Frame(parent)

        inc_nums.grid(row=0, column=0, sticky='nsew', rowspan=4, padx=self._padding, pady=self._padding)
        inc_oprs.grid(row=0, column=1, rowspan=2, sticky='nsew', padx=self._padding, pady=self._padding)
        inc_ptrns.grid(row=2, column=1, sticky='nsew', padx=self._padding, pady=self._padding)
        timers.grid(row=1, column=2, sticky='nsew', padx=self._padding, pady=self._padding)
        username.grid(row=2, column=2, sticky='nsew', padx=self._padding, pady=self._padding)
        num_facts.grid(row=0, column=2, sticky='nsew', padx=self._padding, pady=self._padding)
        delete.grid(row=3, column=2, sticky='nsew', padx=self._padding, pady=self._padding)
        password.grid(row=3, column=1, sticky='nsew', padx=self._padding, pady=self._padding)
        buttons.grid(row=4, column=0, columnspan=3, sticky='nsew', padx=self._padding, pady=self._padding)

        self._inc_nums_frame(inc_nums)
        self._inc_oprs_frame(inc_oprs)
        self._inc_ptrns_frame(inc_ptrns)
        self._timers_frame(timers)
        self._username_frame(username)
        self._num_facts_frame(num_facts)
        self._delete_frame(delete)
        self._password_frame(password)
        self._buttons_frame(buttons)


    def _inc_nums_frame(self, parent):
        
        frame = tk.Frame(parent)
        frame.pack(fill='both', expand=True, padx=4, pady=(4, 10))

        frame.grid_columnconfigure(0, weight=1)
        for i in range(14):
            frame.grid_rowconfigure(i, weight=1)

        label = tk.Label(frame, text="Include Numbers:", font=self._med_font)
        label.grid(row=0, column=0, sticky='w', padx=self._padding, pady=self._padding)

        for i in range(13):
            check = tk.Checkbutton(frame, text=f"Include {i}s", font=self._small_font, variable=self._inc_nums[i])
            check.grid(row=i+1, column=0, sticky='w')


    def _inc_oprs_frame(self, parent):
        
        frame = tk.Frame(parent)
        frame.pack(fill='both', expand=True, padx=self._padding, pady=(4, 10))

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_rowconfigure(2, weight=1)
        frame.grid_rowconfigure(3, weight=1)
        frame.grid_rowconfigure(4, weight=1)

        label = tk.Label(frame, text="Include Operators:", font=self._med_font)
        label.grid(row=0, column=0, sticky='w', padx=self._padding, pady=self._padding)

        names = ["Addition", "Subtraction", "Multiplication", "Division"]
        var_names = ["add", "sub", "mul", "div"]
        for i in range(len(names)):
            check = tk.Checkbutton(frame, text=f"{names[i]}", font=self._small_font, variable=self._inc_oprs[var_names[i]])
            check.grid(row=i+1, column=0, sticky='w')


    def _inc_ptrns_frame(self, parent):

        frame = tk.Frame(parent)
        frame.pack(fill='both', expand=True, padx=self._padding, pady=(4, 10))

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_rowconfigure(2, weight=1)

        label = tk.Label(frame, text="Include Patterns:", font=self._med_font)
        label.grid(row=0, column=0, sticky='w', padx=self._padding, pady=self._padding)

        names = ["Reversed", "Mixed Unknowns"]
        var_names = ["reversed", "mixed_unknowns"]
        for i in range(len(names)):
            check = tk.Checkbutton(frame, text=f"{names[i]}", font=self._small_font, variable=self._inc_ptrns[var_names[i]])
            check.grid(row=i+1, column=0, sticky='w')
        

    def _timers_frame(self, parent):

        frame = tk.Frame(parent)
        frame.pack(fill='both', expand=True, padx=self._padding, pady=self._padding)

        frame.grid_columnconfigure(0, weight=0)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_rowconfigure(2, weight=1)
        frame.grid_rowconfigure(3, weight=1)

        main_label = tk.Label(frame, text="Timer options:", font=self._med_font)
        inc_timers = tk.Checkbutton(frame, text="Include Timers", font=self._small_font, variable=self._inc_timers)
        inc_untimed = tk.Checkbutton(frame, text="Start /w Untimed", font=self._small_font, variable=self._inc_untimed)
        entry_label = tk.Label(frame, text="Values:", font=self._small_font)
        entry = tk.Entry(frame, font=self._small_font, width=1, textvariable=self._timers)
        
        main_label.grid(row=0, column=0, columnspan=2, sticky='w', padx=self._padding, pady=self._padding)
        inc_timers.grid(row=1, column=0, columnspan=2, sticky='w', padx=self._padding, pady=self._padding)
        inc_untimed.grid(row=2, column=0, columnspan=2, sticky='w', padx=self._padding, pady=self._padding)
        entry_label.grid(row=3, column=0, sticky='w', padx=self._padding, pady=self._padding)
        entry.grid(row=3, column=1, sticky='ew', padx=(self._padding, 8), pady=self._padding)

        tog_widgets = [inc_untimed, entry_label, entry]
        self._toggle_timer_widgets(*tog_widgets)
        self._inc_timers.trace_add("write", lambda *args: self._toggle_timer_widgets(*tog_widgets))


    def _delete_frame(self, parent):

        frame = tk.Frame(parent)
        frame.pack(fill='both', expand=True, padx=self._padding, pady=self._padding)
        
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)

        label = tk.Label(frame, text="Delete User:", font=self._med_font)
        delete_button = ttk.Button(frame, text="Delete", style='TButton', command=self._on_delete)
        
        label.grid(row=0, column=0, sticky='w', padx=self._padding, pady=self._padding)
        delete_button.grid(row=1, column=0, padx=self._padding, pady=self._padding)


    def _num_facts_frame(self, parent):
        
        frame = tk.Frame(parent)
        frame.pack(fill='both', expand=True, padx=self._padding, pady=self._padding)

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)

        label = tk.Label(frame, text="Num of Facts:", font=self._med_font)
        entry = tk.Entry(frame, font=self._small_font, width=1, textvariable=self._num_facts)
        
        label.grid(row=0, column=0, sticky='w', padx=self._padding, pady=self._padding)
        entry.grid(row=1, column=0, sticky='ew', padx=(16, 8), pady=self._padding)


    def _username_frame(self, parent):

        frame = tk.Frame(parent)
        frame.pack(fill='both', expand=True, padx=self._padding, pady=(4, 10))

        frame.grid_columnconfigure(0, weight=0)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_rowconfigure(2, weight=1)

        main_label = tk.Label(frame, text="Change Username:", font=self._med_font)
        new_label = tk.Label(frame, text="New Username:", font=self._small_font)
        entry = tk.Entry(frame, textvariable=self._new_username, font=self._small_font, width=1)

        main_label.grid(row=0, column=0, sticky='w', padx=self._padding, pady=self._padding)
        new_label.grid(row=1, column=0, sticky='w', padx=(16, 4))
        entry.grid(row=2, column=0, sticky='ew', padx=(16, 8))


    def _password_frame(self, parent):

        frame = tk.Frame(parent)
        frame.pack(fill='both', expand=True, padx=self._padding, pady=self._padding)
        
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)

        label = tk.Label(frame, text="Reset Password:", font=self._med_font)
        delete_button = ttk.Button(frame, text="Reset", style='TButton', command=self._on_reset)
        
        label.grid(row=0, column=0, sticky='w', padx=self._padding, pady=self._padding)
        delete_button.grid(row=1, column=0, padx=self._padding, pady=self._padding)



    def _buttons_frame(self, parent):
        
        frame = tk.Frame(parent)
        frame.pack(fill='x', side='bottom', padx=self._padding, pady=self._padding)

        save_button = ttk.Button(frame, text="Save", style='TButton', command=self._on_save, width=10)
        cancel_button = ttk.Button(frame, text="Cancel", style='TButton', command=self._on_cancel, width=10)
        save_button.pack(side="right", padx=(10, 0))
        cancel_button.pack(side="right", padx=10)


    def _toggle_timer_widgets(self, *widgets):

        state = 'normal' if self._inc_timers.get() else 'disabled'
        for widget in widgets:
            widget.configure(state=state)


    def _on_delete(self):

        name = self._user.data['user_name']
        message = f'Are you sure you want to delete "{name}"?'
        if messagebox.askyesno("Delete User", message=message):
            self._user.delete_user()
            self.destroy()

    
    def _on_reset(self):

        message = "Are you sure you want to reset your password?"
        if messagebox.askyesno("Reset Password", message=message):
            parent_dir = Path(__file__).resolve().parents[1]
            save_dir = Path.joinpath(parent_dir, 'app_data')
            pass_path = Path.joinpath(save_dir, 'passhash')
            os.remove(pass_path)
            messagebox.showinfo("Password Reset", "Your password has been reset. Don't forget to set a new one.")
            self.destroy()
        

    def _on_save(self):

        new_username = self._new_username.get()
        if new_username:
            old_username = self._user.data['user_name']
            message = f'Are you sure you want to change "{old_username}" to "{new_username}"?'
            if messagebox.askyesno("Change Username", message=message):
                self._user.update_username(new_username)

        if self._new_password.get():
            if messagebox.askyesno("Change Password", message="Are you sure you want to change your password?"):
                new_password = self._new_password.get()
                if new_password:
                    hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
                    self._user.data['password'] = base64.b64encode(hashed_password.encode()).decode()

        if self._save_settings():
            self.destroy()
    

    def _on_cancel(self):

        self.destroy()


    def _load_settings(self):

        settings = copy(self._user.data['settings'])
        
        for k, v in settings['inc_nums'].items():
            self._inc_nums[k] = tk.BooleanVar(value=v)
        for k, v in settings['inc_oprs'].items():
            self._inc_oprs[k] = tk.BooleanVar(value=v)
        for k, v in settings['inc_ptrns'].items():
            self._inc_ptrns[k] = tk.BooleanVar(value=v)
        self._num_facts.set(str(settings['num_facts']))
        self._inc_timers.set(settings['inc_timers'])
        self._inc_untimed.set(settings['inc_untimed'])
        self._timers.set(str(settings['timers'])[1:-1])
        

    def _save_settings(self):

        nf_entry = self._num_facts.get().strip()
        nf_entry_is_valid, message = self._validate_num_facts_entry(nf_entry)
        if not nf_entry_is_valid:
            messagebox.showinfo("Requirements", message)
            return False

        timer_entry = self._timers.get().strip()
        timer_entry_is_valid, message = self._validate_timers_entry(timer_entry)
        if not timer_entry_is_valid:
            messagebox.showinfo("Requirements", message)
            return False

        self._user.save_new_settings({
            'inc_nums': {k: var.get() for k, var in self._inc_nums.items()},
            'inc_oprs': {k: var.get() for k, var in self._inc_oprs.items()},
            'inc_ptrns': {k: var.get() for k, var in self._inc_ptrns.items()},
            'num_facts': int(nf_entry),
            'inc_timers': self._inc_timers.get(),
            'inc_untimed': self._inc_untimed.get(),
            'timers': [int(t) for t in timer_entry.split(",")] })

        return True


    @staticmethod
    def _validate_num_facts_entry(entry):

        analysis = OptionsUI._analyze_stringint(entry, 1, 999)
        if analysis:
            analysis = sorted(analysis, key=len)
            message = "Number of facts should not:\n"
            message += "\n".join(f"  - {err}" for err in analysis)
            
            return False, message
        
        return True, ""


    @staticmethod
    def _validate_timers_entry(entry):

        analysis = set()
        items = entry.split(",")
        for item in items:
            analysis.add(OptionsUI._analyze_stringint(item, 1, 99))
        analysis.discard(None)

        if analysis:
            analysis = sorted(analysis, key=len)
            message = "Timer values elements should not:\n"
            message += "\n".join(f"  - {err}" for err in sorted(analysis, key=len))
            return False, message

        return True, ""


    @staticmethod
    def _analyze_stringint(entry, min_val, max_val):
        
        entry = entry.strip()
        if not entry:
            return f"be empty"

        max_len = len(str(max_val))
        if len(entry) > max_len:
            return f"contain more than {max_len} digits"

        try:
            num = int(entry)
        except ValueError:
            return f"contain non-integer characters"
        
        if num < min_val:
            return f"be less than {min_val}"

        if num > max_val:
            return f"be greater than {max_val}"
    
