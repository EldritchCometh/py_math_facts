
import tkinter as tk

from src.user_manager import UserManager
from src.start_ui import StartUI
from src.facts_manager import FactsManager
from src.game_ui import GameUI



class MathFactsApp(tk.Tk):

    def __init__(self):

        super().__init__()
        self.withdraw()
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        
        self.user = UserManager()
        self.sui = StartUI(self)
        
        self.mainloop()


    def on_start_clicked(self):

        self.sui.withdraw()
        self.facts = FactsManager(self)
        self.gui = GameUI(self)
        self.sui.wait_window(self.gui)
        self.sui.deiconify()


    def on_ready_acknowledged(self, _):
    
        self.gui.set_screen(self.gui.play_screen)


    def on_return(self, event):

        try:
            entry_value = event.widget.get()
            entry_value = int(entry_value)
        except:
            return
        
        if entry_value == self.facts.solution:
            answered_correctly = True
        else:
            answered_correctly = False

        if entry_value != self.facts.solution:
            self.facts.process_submission(answered_correctly)
            self.gui.play_screen.stop_timer()
            return

        self.facts.process_submission(answered_correctly)

        if self.facts.percent_completed < 1.0:
            self.facts.set_next()
            self.gui.set_screen(self.gui.play_screen)
            return

        self.gui.destroy()


    def on_time_up(self):

        self.facts.process_submission(is_correct=False)



mfa = MathFactsApp()
