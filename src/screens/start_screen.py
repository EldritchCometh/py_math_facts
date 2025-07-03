
import tkinter as tk
import tkinter.font as tkFont
from typing import Dict, List, Callable


class StartScreen(tk.Frame):
    def __init__(self, ui):
        super().__init__()
        self.app = ui.app  # Reference to MathFactsApp
        self._ui_frame = tk.Frame(ui)  # Parent frame
        self._frames: Dict[str, tk.Frame] = {}
        self._widgets: Dict[str, tk.Widget] = {}
        self._font = tkFont.Font(family="Arial")  # Font for resizing
        self._after_ids: Dict[str, str] = {}  # For consistency with PlayScreen
        self._make_layout()
        self.populate()

    def populate(self):
        if self._widgets:
            for widget in self._widgets.values():
                widget.destroy()
            self._widgets = {}
        
        label = tk.Label(self._frames['start_frame'], text="Press Enter to Begin", 
                        anchor="center", font=self._font)
        self._widgets['start_label'] = label
        label.pack(expand=True, fill='both')
        label.focus_set()
        label.bind('<Return>', self.app._on_start)
        label.bind('<KP_Enter>', self.app._on_start)

    def resize(self, win_width: Callable[[], int], win_height: Callable[[], int]):
        if not self._widgets:
            return
        width_factor = int(win_width() * 0.08)
        height_factor = int(win_height() * 0.3)
        font_size = min(width_factor, height_factor)
        self._font.configure(size=font_size)

    def _make_layout(self):
        frame = tk.Frame(self._ui_frame, borderwidth=5, relief='raised')
        self._frames['start_frame'] = frame
        self._ui_frame.grid_rowconfigure(0, weight=1)
        self._ui_frame.grid_columnconfigure(0, weight=1)
        frame.grid(row=0, column=0, sticky="nsew", padx=4, pady=4)
        frame.pack_propagate(False)