
from src.math_facts import MathFacts
from src.menu_ui import MenuUI
from src.game_ui import GameUI


class MathFactsApp:


    def __init__(self, settings: dict):

        self.pbs = MathFacts(settings)
        
        self.mui = MenuUI(self)
        self.mui.mainloop()
        
        # self.gui = GameUI(self)
        # self.gui.mainloop()



    def _on_start(self, _):

        self.gui.set_screen(self.gui.play_screen)


    def _on_return(self, event):

        try:
            return_value = event.widget.get()
            return_value = int(return_value)
        except:
            return

        if return_value != self.pbs.solution:
            self.pbs.update_mastery(answered_correctly=False)
            self.gui.play_screen.stop_timer()
            return

        self.pbs.update_mastery(answered_correctly=True)

        if self.pbs.remaining:
            self.pbs.set_next()
            self.gui.set_screen(self.gui.play_screen)
            return

        self.gui.destroy()


    def _on_timeup(self):

        self.pbs.update_mastery(answered_correctly=False)



user_settings = {
    'user': 'user',
    'num_probs': 20,
    'times': [8, 4],
    'exclude': []}
    
mfa = MathFactsApp(user_settings)
