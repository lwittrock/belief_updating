from . import *


class PlayerBot(Bot):
    def play_round(self):
        yield Welcome
        yield Consent, dict(consent=1)
