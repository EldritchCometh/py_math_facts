
from src.ui import MathFactsUI
from src.math_facts import MathFacts



class MathFactsApp:


    def __init__(self, settings: dict):

        self.ps = MathFacts(settings)
        self.ui = MathFactsUI(self)

        self.ui.set_screen_start()
        self.ui.mainloop()


    def _on_start(self, _):

        self.ui.set_screen_play()


    def _on_return(self, event):

        try:
            return_value = event.widget.get()
            return_value = int(return_value)
        except:
            return

        if return_value != self.ps.solution:
            self.ps.update_mastery(answered_correctly=False)
            self.ui.play_screen.stop_timer()
            return

        self.ps.update_mastery(answered_correctly=True)

        if self.ps.remaining:
            self.ps.set_next()
            self.ui.set_screen_play()
            return
        
        self.ui.destroy()


    def _on_timeup(self):

        self.ps.update_mastery(answered_correctly=False)



user_settings = {
    'user': 'user',
    'num_probs': 20,
    'times': [8, 4],
    'exclude': [0, 1]}
    
mfa = MathFactsApp(user_settings)
