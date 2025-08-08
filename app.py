
# todo:
# - add interfaces for everything instead of dictionary access
# - password window changes sizes when label changes
# - shuffle facts_maker facts_manager and user_managers methods
# - refactor factmaker to only produce basic facts
# - implement create_user and num_probs
# - finish implementing settings from usermanager into settings_ui
# - order everything properly in settings_ui
# - remove create from start_ui
# - add create to settings_ui
# - test full grid on settings_ui
# - add num probs to settings_ui
# - add an indent to the text in combobox
# - add return to the entry widgets
# - make sure all entry widgets are focused when the window opens
# - fill in demo stuff in usermanager
# - double check on the last lines in _on_create_clicked in start_ui
# - evaluate whether all of the keys in facts_manager dict are necessary
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


from src.start_ui import StartUI
from src.game_ui import GameUI
from src.user_manager import UserManager
from src.facts_manager import FactsManager



class MathFactsApp:


    def __init__(self):

        self.user = UserManager()
        sui = StartUI(self.user)
        sui.mainloop()
        if not self.user.user_loaded:
            return
        self.facts = FactsManager(self.user)
        self.gui = GameUI(self)
        
        self.gui.mainloop()


    def _on_start(self, _):
    
        self.gui.set_screen(self.gui.play_screen)


    def _on_return(self, event):

        try:
            return_value = event.widget.get()
            return_value = int(return_value)
        except:
            return

        if return_value != self.facts.solution:
            self.facts.update_mastery(answered_correctly=False)
            self.gui.play_screen.stop_timer()
            return

        self.facts.update_mastery(answered_correctly=True)

        if self.facts.remaining:
            self.facts.set_next()
            self.gui.set_screen(self.gui.play_screen)
            return

        self.gui.destroy()


    def _on_timeup(self):

        self.facts.update_mastery(answered_correctly=False)


    
mfa = MathFactsApp()
