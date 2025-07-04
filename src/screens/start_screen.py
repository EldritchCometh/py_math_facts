
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
from typing import Dict, Callable, List


class StartScreen(tk.Frame):
    
    
    def __init__(self, ui):
        
        super().__init__()
        self.app = ui.app  # Reference to MathFactsApp
        
        self._ui_frame = tk.Frame(ui)  # Parent frame
        self._frames: Dict[str, tk.Frame] = {}
        self._widgets: Dict[str, tk.Widget] = {}
        self._big_labels: List[tk.Label] = []
        self._small_labels: List[tk.Label] = []
        self._big_font = tkFont.Font(family="Arial")  # Font for resizing
        self._small_font = tkFont.Font(family="Arial")  # Font for small labels
        self._after_ids: Dict[str, str] = {}  # For consistency with PlayScreen
        
        self._make_layout()
        self.populate()


    def populate(self):

        if self._widgets:
            for widget in self._widgets.values():
                widget.destroy()
            self._widgets = {}
        
        local_font = tkFont.Font(family="Arial", size=12)  # Local font
        # Left: Welcome message
        message = tk.Label(self._frames['message_frame'], 
                          text="Welcome! Start your math practice.", 
                          font=local_font, anchor="center", bg='lightblue')
        self._widgets['message_label'] = message
        message.pack(expand=True, fill='both')

        # Right: Description label
        desc = tk.Label(self._frames['desc_frame'], text="Users:", 
                       font=local_font, anchor="w", bg='lightyellow')
        self._widgets['desc_label'] = desc
        desc.pack(expand=True, fill='both')

        # Right: User dropdown
        users = ["user1", "user2", "user3"]  # Placeholder; load from app_data later
        dropdown = ttk.Combobox(self._frames['dropdown_frame'], values=users, 
                               font=local_font, state="readonly", background='white')
        self._widgets['user_dropdown'] = dropdown
        dropdown.pack(expand=True, fill='both', padx=5, pady=5)  # Added padding for visibility

        # Right: Settings and Start buttons
        settings = tk.Button(self._frames['buttons_frame'], text="Settings", 
                           font=local_font, bg='lightcyan')
        self._widgets['settings_button'] = settings
        settings.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

        start = tk.Button(self._frames['buttons_frame'], text="Start", 
                         font=local_font, bg='lightpink')
        self._widgets['start_button'] = start
        start.grid(row=0, column=1, sticky="nsew", padx=2, pady=2)


    def _make_layout(self):

        self._ui_frame.grid_rowconfigure(0, weight=1)  # One row
        self._ui_frame.grid_columnconfigure(0, weight=2)  # Left column, weight 2
        self._ui_frame.grid_columnconfigure(1, weight=1)  # Right column, weight 1

        # Left column frame (entry message space)
        left_frame = tk.Frame(self._ui_frame, borderwidth=5, relief='raised', bg='lightblue')
        self._frames['message_frame'] = left_frame
        left_frame.grid(row=0, column=0, sticky="nsew", padx=4, pady=4)
        left_frame.pack_propagate(False)

        # Right column frame (container for rows)
        right_frame = tk.Frame(self._ui_frame, borderwidth=5, relief='raised', bg='lightgreen')
        self._frames['right_frame'] = right_frame
        right_frame.grid(row=0, column=1, sticky="nsew", padx=4, pady=4)
        right_frame.pack_propagate(False)

        # Subdivide right frame into 3 rows
        right_frame.grid_rowconfigure(0, weight=1)  # Description
        right_frame.grid_rowconfigure(1, weight=1)  # Dropdown
        right_frame.grid_rowconfigure(2, weight=1)  # Buttons
        right_frame.grid_columnconfigure(0, weight=1)

        # Row 0: Description label
        desc_frame = tk.Frame(right_frame, borderwidth=2, relief='flat', bg='lightyellow')
        self._frames['desc_frame'] = desc_frame
        desc_frame.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        desc_frame.pack_propagate(False)

        # Row 1: User dropdown
        dropdown_frame = tk.Frame(right_frame, borderwidth=2, relief='flat', bg='lightcyan')
        self._frames['dropdown_frame'] = dropdown_frame
        dropdown_frame.grid(row=1, column=0, sticky="nsew", padx=2, pady=2)
        dropdown_frame.pack_propagate(False)

        # Row 2: Buttons (settings and start)
        buttons_frame = tk.Frame(right_frame, borderwidth=2, relief='flat', bg='lightpink')
        self._frames['buttons_frame'] = buttons_frame
        buttons_frame.grid(row=2, column=0, sticky="nsew", padx=2, pady=2)
        buttons_frame.pack_propagate(False)
        buttons_frame.grid_columnconfigure(0, weight=1)  # Settings button
        buttons_frame.grid_columnconfigure(1, weight=1)  # Start button
    
    
    def resize(self, win_width: Callable, win_height: Callable):
        
        if not self._widgets:
            return
        
        width_factor = int(win_width() * 0.08)
        height_factor = int(win_height() * 0.3)
        font_size = min(width_factor, height_factor)
        self._font.configure(size=font_size)
