
# todo:
# - spell check all dialogue messages
# - see if i can make clicking on the combobox highlight all text
# - make it more difficult to hack than just deleting the password file
# - put all the stuff in options_ui in the right order
# - make the order in settings match the order in options_ui
# - maybe use fuller names for methods in options_ui
# - maybe add explicit types everywhere
# - address all lines over 80 characters
# - sometimes select is highlighted in select username when I leave options_ui
# - change timers to timer_vals
# - probe and test accurate recording of progress
# - make the start button in start_ui call a method in MathFactsApp
# - look into closing options_ui always deselecting the combobox
# - turn the password back on
# - add a results screen
# - ready_screen label too close to horozontal walls
# - add a cencel button to password_ui
# - check for using all imported modules
# - fix 4 level indentation in _is_mastered


import tkinter as tk

from src.start_ui import StartUI
from src.game_ui import GameUI
from src.user_manager import UserManager
from src.facts_manager import FactsManager



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
