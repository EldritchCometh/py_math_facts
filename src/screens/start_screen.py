
import tkinter as tk
import tkinter.font as tkFont
from src.screens.resources.message_widths \
    import REFERENCE_DPI, START_MESSAGE_WIDTHS, MESSAGE_HEIGHTS


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

        dpi_ratio = self.winfo_fpixels('1i') / REFERENCE_DPI
        ws_dict = {k: v * dpi_ratio for k, v in START_MESSAGE_WIDTHS.items()}
        width_target = self._start_message_frame.winfo_width()

        w_font = max((k for k, v in ws_dict.items() if v <= width_target))
        new_font_size = int(w_font)
        self._font.configure(size=max(10, new_font_size))




    # def resize(self):

    #     w_target = self._start_message_frame.winfo_width()
    #     #h_target = self._start_message_frame.winfo_height()

    #     #print(w_target)

    #     dpi = self.winfo_fpixels('1i')
    #     ws_dict = {k: v * dpi for k, v in START_MESSAGE_WIDTHS.items()}
    #     #hs_dict = {k: v * dpi for k, v in MESSAGE_HEIGHTS.items()}

    #     #print(ws_dict)

    #     w_font = max((k for k, v in ws_dict.items() if v <= w_target))
    #     #h_font = max((k for k, v in hs_dict.items() if v <= h_target))

    #     w_font = ws_dict[5]

    #     new_font_size = int(w_font)
    #     self._font.configure(size=max(10, new_font_size))





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