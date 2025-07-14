
from src.math_facts import MathFacts
from src.start_ui import StartUI
from src.game_ui import GameUI


class MathFactsApp:


    def __init__(self, settings: dict):

        self.mfs = MathFacts(settings)

        # self.sui = StartUI(self)
        # self.sui.mainloop()

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

        if return_value != self.mfs.solution:
            self.mfs.update_mastery(answered_correctly=False)
            self.gui.play_screen.stop_timer()
            return

        self.mfs.update_mastery(answered_correctly=True)

        if self.mfs.remaining:
            self.mfs.set_next()
            self.gui.set_screen(self.gui.play_screen)
            return

        self.gui.destroy()


    def _on_timeup(self):

        self.mfs.update_mastery(answered_correctly=False)



user_settings = {
    'user': 'user',
    'num_facts': 20,
    'times': [8, 4],
    'exclude': []}
    
mfa = MathFactsApp(user_settings)
