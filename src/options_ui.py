
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkfont
import string
from pathlib import Path

from src.utils import sha256_hash



class OptionsUI(tk.Toplevel):


    def __init__(self, user):

        super().__init__()
        
        self._user = user

        self.title("Math Facts Settings")
        self.attributes('-type', 'dialog')

        self._pad = 4
        self._border_width = 4
        self._entry_widget_width = 10

        default_font = tkfont.nametofont("TkDefaultFont")
        self._big_font = tkfont.Font(
            family=default_font.actual()["family"], size=42, weight="bold")
        self._med_font = tkfont.Font(
            family=default_font.actual()["family"], size=14)
        self._small_font = tkfont.Font(
            family=default_font.actual()["family"], size=12)

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
        self._timer_vals = tk.StringVar()
        self._new_username = tk.StringVar()
        self._new_password = tk.StringVar()
        self._load_settings()

        self._main_frame = tk.Frame(self)
        self._make_layout(self._main_frame)
        self._main_frame.pack(expand=True, fill="both", padx=self._pad, pady=self._pad)


    def _make_layout(self, parent) -> None:

        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        parent.grid_columnconfigure(2, weight=1)
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_rowconfigure(1, weight=1)
        parent.grid_rowconfigure(2, weight=1)
        parent.grid_rowconfigure(3, weight=1)
        parent.grid_rowconfigure(4, weight=1)

        inc_nums = tk.Frame(parent, bd=self._border_width, relief="groove")
        inc_oprs = tk.Frame(parent, bd=self._border_width, relief="groove")
        inc_ptrns = tk.Frame(parent, bd=self._border_width, relief="groove")
        num_facts = tk.Frame(parent, bd=self._border_width, relief="groove")
        timer_opts = tk.Frame(parent, bd=self._border_width, relief="groove")
        username = tk.Frame(parent, bd=self._border_width, relief="groove")
        password = tk.Frame(parent, bd=self._border_width, relief="groove")
        delete = tk.Frame(parent, bd=self._border_width, relief="groove")
        buttons = tk.Frame(parent)

        grid_opts = {'sticky': 'nsew', 'padx': self._pad, 'pady': self._pad}
        inc_nums.grid(row=0, column=0, rowspan=4, **grid_opts)
        inc_oprs.grid(row=0, column=1, rowspan=2, **grid_opts)
        inc_ptrns.grid(row=2, column=1, **grid_opts)
        num_facts.grid(row=0, column=2, **grid_opts)
        timer_opts.grid(row=1, column=2, **grid_opts)
        username.grid(row=2, column=2, **grid_opts)
        password.grid(row=3, column=1, **grid_opts)
        delete.grid(row=3, column=2, **grid_opts)
        buttons.grid(row=4, column=0, columnspan=3, **grid_opts)

        self._include_numbers_frame(inc_nums)
        self._include_operators_frame(inc_oprs)
        self._include_patterns_frame(inc_ptrns)
        self._timer_options_frame(timer_opts)
        self._change_username_frame(username)
        self._num_of_facts_frame(num_facts)
        self._reset_password_frame(password)
        self._delete_user_frame(delete)
        self._main_buttons_frame(buttons)


    def _include_numbers_frame(self, parent) -> None:
        
        frame = tk.Frame(parent)
        frame.pack(fill='both', expand=True, padx=4, pady=(4, 10))

        frame.grid_columnconfigure(0, weight=1)
        for i in range(14):
            frame.grid_rowconfigure(i, weight=1)

        label = tk.Label(frame, text="Include Numbers:", font=self._med_font)
        label.grid(row=0, column=0, sticky='w', padx=self._pad, pady=self._pad)

        for i in range(13):
            check = tk.Checkbutton(
                frame, text=f"Include {i}s", font=self._small_font, 
                variable=self._inc_nums[i])
            check.grid(row=i+1, column=0, sticky='w')


    def _include_operators_frame(self, parent) -> None:
        
        frame = tk.Frame(parent)
        frame.pack(fill='both', expand=True, padx=self._pad, pady=(4, 10))

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_rowconfigure(2, weight=1)
        frame.grid_rowconfigure(3, weight=1)
        frame.grid_rowconfigure(4, weight=1)

        label = tk.Label(frame, text="Include Operators:", font=self._med_font)
        label.grid(row=0, column=0, sticky='w', padx=self._pad, pady=self._pad)

        names = ["Addition", "Subtraction", "Multiplication", "Division"]
        var_names = ["add", "sub", "mul", "div"]
        for i in range(len(names)):
            check = tk.Checkbutton(
                frame, text=f"{names[i]}", font=self._small_font, 
                variable=self._inc_oprs[var_names[i]])
            check.grid(row=i+1, column=0, sticky='w')


    def _include_patterns_frame(self, parent) -> None:

        frame = tk.Frame(parent)
        frame.pack(fill='both', expand=True, padx=self._pad, pady=(4, 10))

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_rowconfigure(2, weight=1)

        label = tk.Label(frame, text="Include Patterns:", font=self._med_font)
        label.grid(row=0, column=0, sticky='w', padx=self._pad, pady=self._pad)

        names = ["Reversed", "Mixed Unknowns"]
        var_names = ["reversed", "mixed_unknowns"]
        for i in range(len(names)):
            check = tk.Checkbutton(
                frame, text=f"{names[i]}", font=self._small_font, 
                variable=self._inc_ptrns[var_names[i]])
            check.grid(row=i+1, column=0, sticky='w')
        

    def _timer_options_frame(self, parent) -> None:

        frame = tk.Frame(parent)
        frame.pack(fill='both', expand=True, padx=self._pad, pady=self._pad)

        frame.grid_columnconfigure(0, weight=0)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_rowconfigure(2, weight=1)
        frame.grid_rowconfigure(3, weight=1)

        main_label = tk.Label(frame, text="Timer options:", font=self._med_font)
        inc_timers = tk.Checkbutton(
            frame, text="Include Timers", font=self._small_font, 
            variable=self._inc_timers)
        inc_untimed = tk.Checkbutton(
            frame, text="Start /w Untimed", font=self._small_font, 
            variable=self._inc_untimed)
        entry_label = tk.Label(frame, text="Values:", font=self._small_font)
        entry = tk.Entry(
            frame, font=self._small_font, width=1, 
            textvariable=self._timer_vals)
        
        grid_opts = \
            {'sticky': 'w', 'padx': self._pad, 'pady': self._pad}
        main_label.grid(row=0, column=0, columnspan=2, **grid_opts)
        inc_timers.grid(row=1, column=0, columnspan=2, **grid_opts)
        inc_untimed.grid(row=2, column=0, columnspan=2, **grid_opts)
        entry_label.grid(row=3, column=0, **grid_opts)
        entry.grid(
            row=3, column=1, sticky='ew', padx=(self._pad, 8), pady=self._pad)

        tog_widgets = [inc_untimed, entry_label, entry]
        self._toggle_timer_widgets(*tog_widgets)
        self._inc_timers.trace_add(
            "write", lambda *args: self._toggle_timer_widgets(*tog_widgets))


    def _change_username_frame(self, parent) -> None:

        frame = tk.Frame(parent)
        frame.pack(fill='both', expand=True, padx=self._pad, pady=(4, 10))

        frame.grid_columnconfigure(0, weight=0)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_rowconfigure(2, weight=1)

        main_label = tk.Label(
            frame, text="Change Username:", font=self._med_font)
        new_label = tk.Label(
            frame, text="New Username:", font=self._small_font)
        entry = tk.Entry(
            frame, textvariable=self._new_username, 
            font=self._small_font, width=1)

        main_label.grid(
            row=0, column=0, sticky='w', padx=self._pad, pady=self._pad)
        new_label.grid(row=1, column=0, sticky='w', padx=(16, 4))
        entry.grid(row=2, column=0, sticky='ew', padx=(16, 8))


    def _num_of_facts_frame(self, parent) -> None:
        
        frame = tk.Frame(parent)
        frame.pack(fill='both', expand=True, padx=self._pad, pady=self._pad)

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)

        label = tk.Label(frame, text="Num of Facts:", font=self._med_font)
        entry = tk.Entry(
            frame, font=self._small_font, width=1, textvariable=self._num_facts)
        
        label.grid(row=0, column=0, sticky='w', padx=self._pad, pady=self._pad)
        entry.grid(row=1, column=0, sticky='ew', padx=(16, 8), pady=self._pad)


    def _reset_password_frame(self, parent) -> None:

        frame = tk.Frame(parent)
        frame.pack(fill='both', expand=True, padx=self._pad, pady=self._pad)
        
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)

        label = tk.Label(frame, text="Reset Password:", font=self._med_font)
        delete_button = ttk.Button(
            frame, text="Reset", style='TButton', command=self._on_reset)
        
        label.grid(row=0, column=0, sticky='w', padx=self._pad, pady=self._pad)
        delete_button.grid(row=1, column=0, padx=self._pad, pady=self._pad)


    def _delete_user_frame(self, parent) -> None:

        frame = tk.Frame(parent)
        frame.pack(fill='both', expand=True, padx=self._pad, pady=self._pad)
        
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)

        label = tk.Label(frame, text="Delete User:", font=self._med_font)
        delete_button = ttk.Button(
            frame, text="Delete", style='TButton', command=self._on_delete)
        
        label.grid(row=0, column=0, sticky='w', padx=self._pad, pady=self._pad)
        delete_button.grid(row=1, column=0, padx=self._pad, pady=self._pad)


    def _main_buttons_frame(self, parent) -> None:
        
        frame = tk.Frame(parent)
        frame.pack(fill='x', side='bottom', padx=self._pad, pady=self._pad)

        save_button = ttk.Button(
            frame, text="Save", style='TButton', 
            command=self._on_save, width=10)
        cancel_button = ttk.Button(
            frame, text="Cancel", style='TButton', 
            command=self._on_cancel, width=10)
        save_button.pack(side="right", padx=(10, 0))
        cancel_button.pack(side="right", padx=10)


    def _on_reset(self) -> None:

        message = "Are you sure you want to reset your password?"
        if messagebox.askyesno("Reset Password", message=message):
            parent_dir = Path(__file__).resolve().parents[1]
            save_dir = Path.joinpath(parent_dir, 'data')
            pass_path = Path.joinpath(save_dir, 'passhash')
            default_passhash = sha256_hash('mathfacts')
            with open(pass_path, 'w') as f:
                f.write(default_passhash)
            messagebox.showinfo("Password Reset", 
                                "Your password has been reset.")


    def _on_delete(self) -> None:

        message = f'Are you sure you want to delete "{self._user.user_name}"?'
        if messagebox.askyesno("Delete User", message=message):
            self._user.delete_current_user()
            self.destroy()
        

    def _on_save(self) -> None:

        if self._save_settings():
            self.destroy()
    

    def _on_cancel(self) -> None:

        self.destroy()


    def _toggle_timer_widgets(self, *widgets) -> None:

        state = 'normal' if self._inc_timers.get() else 'disabled'
        for widget in widgets:
            widget.configure(state=state)


    def _load_settings(self) -> None:
        
        for k, v in self._user.inc_nums.items():
            self._inc_nums[k] = tk.BooleanVar(value=v)
        for k, v in self._user.inc_oprs.items():
            self._inc_oprs[k] = tk.BooleanVar(value=v)
        for k, v in self._user.inc_ptrns.items():
            self._inc_ptrns[k] = tk.BooleanVar(value=v)
        self._num_facts.set(str(self._user.num_facts))
        self._inc_timers.set(self._user.inc_timers)
        self._inc_untimed.set(self._user.inc_untimed)
        self._timer_vals.set(str(self._user.timer_vals)[1:-1])
       

    def _save_settings(self) -> bool:

        nf_entry = self._num_facts.get().strip()
        nf_entry_is_valid, message = self._validate_num_facts_entry(nf_entry)
        if not nf_entry_is_valid:
            messagebox.showinfo("Requirements", message)
            return False

        timer_entry = self._timer_vals.get().strip()
        timer_entry_is_valid, message = self._validate_timers_entry(timer_entry)
        if not timer_entry_is_valid:
            messagebox.showinfo("Requirements", message)
            return False
        
        new_username = self._new_username.get().strip()
        if new_username:
            valid, errs = self._validate_username(new_username)
        if new_username and errs:
            message = "Username should:\n"
            message += "\n".join(f"  - {err}" for err in errs)
            messagebox.showinfo("Requirements", message)
            return False
        if new_username and not valid:
            return False
        if new_username:
            old_username = self._user.user_name
            message = f'Are you sure you want to change \
                "{old_username}" to "{new_username}"?'
            if messagebox.askyesno("Change Username", message=message):
                self._user.delete_current_user()
                self._user.user_name = new_username
                
        self._user.inc_nums = \
            {k: var.get() for k, var in self._inc_nums.items()}
        self._user.inc_oprs = \
            {k: var.get() for k, var in self._inc_oprs.items()}
        self._user.inc_ptrns = \
            {k: var.get() for k, var in self._inc_ptrns.items()}
        self._user.num_facts = int(nf_entry)
        self._user.inc_timers = self._inc_timers.get()
        self._user.inc_untimed = self._inc_untimed.get()
        self._user.timer_vals = [int(t) for t in timer_entry.split(",")]
        self._user.save_user_data()

        return True


    @staticmethod
    def _validate_num_facts_entry(entry) -> tuple[bool, str]:

        analysis = OptionsUI._analyze_stringint(entry, 1, 999)
        if analysis:
            analysis = sorted(analysis, key=len)
            message = "Number of facts should not:\n"
            message += "\n".join(f"  - {err}" for err in analysis)
            
            return False, message
        
        return True, ""


    @staticmethod
    def _validate_timers_entry(entry) -> tuple[bool, str]:

        analysis = set()
        items = entry.split(",")
        for item in items:
            analysis.add(OptionsUI._analyze_stringint(item, 1, 99))
        analysis.discard("")

        if analysis:
            analysis = sorted(analysis, key=len)
            message = "Timer values elements should not:\n"
            message += "\n".join(f"  - {err}" for err in analysis)
            return False, message

        return True, ""


    @staticmethod
    def _analyze_stringint(entry, min_val, max_val) -> str:
        
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
        
        return ""
    

    def _validate_username(self, cbbox_val: str) -> tuple[bool, list[str]]:

        if not cbbox_val.strip():
            return False, ["Username cannot be empty"]
        if cbbox_val.strip() == "Select User":
            return False, []
        if cbbox_val in self._user.get_saved_users():
            return False, []

        errs = []
        if not cbbox_val[0].isalpha():
            errs.append("begin with a letter")
        if not any(c in string.ascii_letters for c in cbbox_val):
            errs.append("contain at least one letter")
        if any(c.isspace() for c in cbbox_val):
            errs.append("not contain whitespace")
        if len(cbbox_val) < 2:
            errs.append("be at least two characters long")
        whitelist = string.ascii_letters + string.digits + '_'
        if not all(c in whitelist for c in cbbox_val):
            errs.append("contain only letters, digits or underscores")
        
        if errs:
            return False, errs
        else:
            return True, []