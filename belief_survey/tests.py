from . import *
import random

class PlayerBot(Bot):
    def play_round(self):
        if self.round_number == 1:
            yield Instructions, dict(test1=1, test2=2, test3=3, test4=3, test5=3, test6=1, sr_button_clicks=3)
            yield InstructionsFeedback
            yield UrnDraw
            yield BeliefInput, dict(belief=random.randint(0, 100), info_button_clicks=random.randint(0, 5))
        else:
            yield BeliefInput, dict(belief=random.randint(0, 100), info_button_clicks=random.randint(0, 5))

