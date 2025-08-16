
import tkinter as tk
import tkinter.font as tkFont



class ReadyScreen(tk.Frame):

   
    def __init__(self, gui):

        super().__init__(gui)

        self.gui = gui
        self.app = gui.app

        self._gui_frame = tk.Frame(gui)
        self._start_message_frame: tk.Frame
        self._font = tkFont.Font(family="Arial")
        self._start_message = "Press enter to begin!"
        self._window_size = (0, 0)
        
        self._make_layout()


    def _make_layout(self) -> None:

        self._start_message_frame = tk.Frame(self._gui_frame)
        self._start_message_frame.pack(expand=True, fill='both')


    def populate(self) -> None:

        start_message_label = tk.Label(
            self._start_message_frame, text=self._start_message, 
            font=self._font)
        start_message_label.pack(expand=True, fill='both')
        start_message_label.focus_set()
        start_message_label.bind('<Return>', self.app.on_ready_acknowledged)
        start_message_label.bind('<KP_Enter>', self.app.on_ready_acknowledged)


    def resize(self) -> None:

        new_window_size = (self.gui.winfo_width(), self.gui.winfo_height())
        if new_window_size == self._window_size:
            return
        self._window_size = new_window_size

        small_font_size = 10
        small_font = tkFont.Font(family="Arial", size=small_font_size)
        small_width = small_font.measure(self._start_message)
        small_height = small_font.metrics('linespace')
        
        large_font_size = 100
        large_font = tkFont.Font(family="Arial", size=large_font_size)
        large_width = large_font.measure(self._start_message)
        large_height = large_font.metrics('linespace')

        target_width = self._start_message_frame.winfo_width()
        ratio = (target_width - small_width) / (large_width - small_width)
        w_size = small_font_size + ratio * (large_font_size - small_font_size)
        w_size *= self.gui.winfo_fpixels('1i') / 96 * 0.95

        target_height = self._start_message_frame.winfo_height()
        ratio = (target_height - small_height) / (large_height - small_height)
        h_size = small_height + ratio * (large_height - small_height)
        h_size *= self.gui.winfo_fpixels('1i') / 96 * 0.35

        final_size = min(int(w_size), int(h_size))
        self._font.configure(size=final_size)

