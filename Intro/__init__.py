from otree.api import *

author = 'Lars Wittrock'

doc = """
Intro to the study
"""


class Constants(BaseConstants):
    name_in_url = 'Intro'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    consent = models.BooleanField(
        widget=widgets.CheckboxInput(),
        label="I agree.",
    )

    is_mobile = models.BooleanField(doc="Automatic check through JS whether gadget is phone or not")

    prolific_id = models.CharField(
        initial='',
        label="Prolific ID:",
    )

    #starting_time = models.LongStringField(doc="Time at which experiment starts") - to implement

    # Error messages
    @staticmethod
    def consent_error_message(value):
        print('value is', value)
        if value != 1:
            return 'Your confirmation is required to proceed.'

    @staticmethod
    def prolific_id_error_message(value):
        print('value is', value)
        if value == '':
            return 'Your Prolific ID is required to proceed.'


# PAGES

class Welcome(Page):
    form_model = 'player'
    form_fields = ['is_mobile']


class SorryNoPhone(Page):
    @staticmethod
    def is_displayed(player):
        return player.is_mobile == 1


class Consent(Page):
    form_model = 'player'
    form_fields = ['consent']


class ProlificID(Page):
    form_model = 'player'
    form_fields = ['prolific_id']


page_sequence = [Welcome, SorryNoPhone, Consent, ProlificID]
