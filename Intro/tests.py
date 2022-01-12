from . import *


class PlayerBot(Bot):
    def play_round(self):
        yield Welcome, dict(is_mobile=0, welcome_button_clicks=0)
        yield Consent, dict(consent=1)
