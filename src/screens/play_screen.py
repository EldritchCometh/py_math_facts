
import time
import tkinter as tk
from tkinter import ttk
from typing import Dict, List, Callable
import tkinter.font as tkFont


class PlayScreen(tk.Frame):
    

    def __init__(self, ui):

        super().__init__()
        
        self.app = ui.app
        self.ps = ui.app.ps

        self._ui_frame = tk.Frame(ui)
        self._frames: Dict[str, tk.Frame] = {}
        self._eq_sub_frames: List[tk.Frame] = []
        self._widgets: Dict[str, tk.Widget] = {}
        self._font = tkFont.Font(family="Arial")
        self._after_ids = {}

        self._make_layout()


    def populate(self):

        if self._widgets:
            for widget in self._widgets.values():
                widget.destroy()
            self._widgets = {}
        
        for i, (t, f) in enumerate(zip(self.ps.equation, self._eq_sub_frames)):
            if t == '_':
                widget = tk.Entry(f, width=3, justify='center', font=self._font)
                self._widgets['entry'] = widget
                widget.focus_set()
            else:
                widget = tk.Label(f, text=t, font=self._font)
                self._widgets[f'labels_{i}'] = widget
        
        prog_bar_names = ['timer', 'progress', 'mastery']
        values = [0, self.ps.percent_completed, self.ps.percent_mastered]
        for name, v in zip(prog_bar_names, values):
            bar = ttk.Progressbar(self._frames[f'{name}_frame'])
            bar.configure(orient='horizontal', mode='determinate')
            self._widgets[f'{name}_bar'] = bar
            bar['maximum'], bar['value'] = 1000, v * 1000
        
        self._start_timer()
        self._widgets['entry'].bind('<Return>', self.app._on_return)
        self._widgets['entry'].bind('<KP_Enter>', self.app._on_return)

        for widget in self._widgets.values():
            widget.pack(expand=True, fill='both')


    def resize(self, win_width: Callable, win_height: Callable):

        if not self._widgets:
            return
        
        eq_frame_height = win_height() * (1-3/8)
        width_factor = int(win_width() * 0.1)
        height_factor = int(eq_frame_height * 1)
        font_size = min(width_factor, height_factor)
        self._font.configure(size=font_size)
        

    def stop_timer(self):
        
        if 'update_timer' in self._after_ids:
            after_id = self._after_ids.pop('update_timer')
            if after_id is not None:
                self._ui_frame.after_cancel(after_id)


    def _start_timer(self):
        
        self.stop_timer()
        timer_bar = self._widgets['timer_bar']
        timer_bar['maximum'] = self.ps.timer_duration
        timer_bar['value'] = 0
        self._start_time = time.time()

        if self.ps.timer_duration == 0:
            return

        def update_timer():
            elapsed = time.time() - self._start_time
            timer_bar['value'] = elapsed
            if elapsed < self.ps.timer_duration:
                self._after_ids['update_timer'] = \
                    self._ui_frame.after(10, update_timer)
            else:
                timer_bar['value'] = self.ps.timer_duration
                self.app._on_timeup()

        update_timer()


    def _make_layout(self):

        frame_names = ['equation_frame', 'timer_frame', 
                       'progress_frame', 'mastery_frame']
        row_weights = [8, 1, 1, 1]
        frame_padys = [(4, 2), (2, 2), (2, 2), (2, 2)]
        arg_lists = zip(frame_names, row_weights, frame_padys)
        self._ui_frame.grid_columnconfigure(0, weight=1)
        for i, (name, weight, pady) in enumerate(arg_lists):
            frame = tk.Frame(self._ui_frame, borderwidth=5, relief='raised')
            self._frames[name] = frame
            self._ui_frame.grid_rowconfigure(i, weight=weight)    
            frame.grid(row=i, column=0, sticky="nsew", padx=4, pady=pady)
            frame.pack_propagate(False)
            
        eq_inner_frame = tk.Frame(self._frames['equation_frame'])
        self._eq_sub_frames = [tk.Frame(eq_inner_frame) for _ in range(5)]
        eq_inner_frame.grid_rowconfigure(0, weight=1)
        for i, sf in enumerate(self._eq_sub_frames):
            eq_inner_frame.grid_columnconfigure(i, weight=1)
            sf.grid(row=0, column=i, sticky="nsew", padx=2, pady=2)
        eq_inner_frame.pack(expand=True, fill='both')
