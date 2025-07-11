
from src.game_ui.game_ui import GameUI
from src.menu_ui.menu_ui import MenuUI
from src.math_facts import MathFacts



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

        if return_value != self.ps.solution:
            self.ps.update_mastery(answered_correctly=False)
            self.ui.play_screen.stop_timer()
            return

        self.ps.update_mastery(answered_correctly=True)

        if self.ps.remaining:
            self.ps.set_next()
            self.ui.set_screen(self.ui.play_screen)
            return

        self.ui.destroy()


    def _on_timeup(self):

        self.ps.update_mastery(answered_correctly=False)



user_settings = {
    'user': 'user',
    'num_probs': 20,
    'times': [8, 4],
    'exclude': []}
    
mfa = MathFactsApp(user_settings)
