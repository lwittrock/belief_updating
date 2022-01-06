from . import *


class PlayerBot(Bot):
    def play_round(self):
        yield Instructions, dict(test1=1, test2=2, test3=3, test4=3, test5=3, test6=1)
        expect(self.player.test_score, 6)
        yield InstructionsFeedback
        yield UrnDraw
        yield BeliefInput, dict(belief=random.uniform(0, 1))
