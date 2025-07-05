
import tkinter as tk
import tkinter.font as tkFont
from src.screens.resources.message_widths \
    import START_MESSAGE_WIDTHS, MESSAGE_HEIGHTS


class StartScreen(tk.Frame):

   
    def __init__(self, ui):

        super().__init__(ui)

        self.app = ui.app

        self._ui_frame = tk.Frame(ui)
        self._start_message_frame: tk.Frame
        self._font = tkFont.Font(family="Arial")
        self._start_message = "Press enter to begin!"
        self._make_layout()


    def populate(self):

        start_message_label = tk.Label(
            self._start_message_frame, text=self._start_message, 
            font=self._font)
        start_message_label.pack(expand=True, fill='both')
        start_message_label.focus_set()
        start_message_label.bind('<Return>', self.app._on_start)
        start_message_label.bind('<KP_Enter>', self.app._on_start)


    def _make_layout(self):

        self._start_message_frame = tk.Frame(self._ui_frame)
        self._start_message_frame.pack(expand=True, fill='both')


    def resize(self):
       
        ws_dict = START_MESSAGE_WIDTHS.items()
        hs_dict = MESSAGE_HEIGHTS.items()

        w_target = self._start_message_frame.winfo_width() * 0.9
        h_target = self._start_message_frame.winfo_height() * 0.9

        w_font = max((k for k, v in ws_dict if v <= w_target))
        h_font = max((k for k, v in hs_dict if v <= h_target))

        new_font_size = int(min(w_font, h_font) * 0.85)
        self._font.configure(size=max(10, new_font_size))












    # def resize(self):

    #     target = self._start_message_frame.winfo_height()
    #     self._font.configure(size=1)
    #     low, high = 10, 500
    #     while low <= high:
    #         mid = (low + high) // 2
    #         self._font.configure(size=mid)
    #         mid_height = self._font.metrics('linespace')
    #         if mid_height > target:
    #             high = mid - 1
    #         else:
    #             low = mid + 1
    #     height = high

    #     target = self._start_message_frame.winfo_width()
    #     self._font.configure(size=1)
    #     low, high = 10, 500
    #     while low <= high:
    #         mid = (low + high) // 2
    #         self._font.configure(size=mid)
    #         mid_width = START_MESSAGE_WIDTHS[mid]
    #         if mid_width > target:
    #             high = mid - 1
    #         else:
    #             low = mid + 1
    #     width = high

    #     size = min(width, height)
    #     self._font.configure(size=size)