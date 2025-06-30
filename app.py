
from dataclasses import dataclass
from src.ui import MathFactsUI
from src.math_facts import MathFacts



class MathFactsApp:


    def __init__(self, settings: dict):

        self.ps = MathFacts(settings)
        self.ui = MathFactsUI(self)

        self.ui.set_screen_play()
        self.ui.mainloop()


    def _on_return(self, event):

        try:
            return_value = event.widget.get()
            return_value = int(return_value)
        except:
            return

        if return_value != self.ps.solution:
            self.ps.update_progress(answered_correctly=False)
            self.ui.play_screen.stop_timer()
            return

        self.ps.update_progress(answered_correctly=True)
        
        if self.ps.facts_remaining:
            self.ps.set_next()
            self.ui.set_screen_play()
            return
        
        self.ui.destroy()


    def _on_timeup(self):
        
        self.ps.update_progress(answered_correctly=False)



penny_settings = {
    'user': 'penny',
    'num_probs': 10,
    'times': [0]}

clemmie_settings = {
    'user': 'clemmie',
    'num_probs': 100,
    'times': [8, 4]}

test_settings = {
    'user': 'tester',
    'num_probs': 10,
    'times': [8, 4]}
    
mfa = MathFactsApp(test_settings)