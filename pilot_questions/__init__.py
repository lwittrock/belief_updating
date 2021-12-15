from otree.api import *

author = 'Lars Wittrock'

doc = """
This app collects feedback on the setup from participants during a pilot. Not part of the main study.
"""


class Constants(BaseConstants):
    name_in_url = 'pilot_questions'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # on instructions
    instructions_clear = models.IntegerField(doc='clarity of instructions',
                                             label='The instructions in the beginning were clear to me.',
                                             choices=[
                                                 [1, 'Strongly disagree.'],
                                                 [2, 'Disagree.'],
                                                 [3, 'Neither agree nor disagree.'],
                                                 [4, 'Agree.'],
                                                 [5, 'Strongly agree.']
                                             ])
    instructions_improve = models.LongStringField(doc='Improvement for instructions',
                                                  label='What do you think was unclear/ could be improved regarding the instructions?')
    # on task
    task_clear = models.IntegerField(doc='clarity of instructions',
                                     label='The main task and the way information was presented were clear to me.',
                                     choices=[
                                         [1, 'Strongly disagree.'],
                                         [2, 'Disagree.'],
                                         [3, 'Neither agree nor disagree.'],
                                         [4, 'Agree.'],
                                         [5, 'Strongly agree.']
                                     ])
    task_interesting = models.IntegerField(doc='clarity of instructions',
                                           label='I thought guessing the urn was interesting/ enjoyable.',
                                           choices=[
                                               [1, 'Strongly disagree.'],
                                               [2, 'Disagree.'],
                                               [3, 'Neither agree nor disagree.'],
                                               [4, 'Agree.'],
                                               [5, 'Strongly agree.']
                                           ])
    task_difficult = models.IntegerField(doc='clarity of instructions',
                                         label="I thought guessing the urn was (too) difficult.",
                                         choices=[
                                             [1, 'Strongly disagree.'],
                                             [2, 'Disagree.'],
                                             [3, 'Neither agree nor disagree.'],
                                             [4, 'Agree.'],
                                             [5, 'Strongly agree.']
                                         ])
    task_improve = models.LongStringField(doc='Feedback regarding task',
                                          label="What do you think was unclear/ could be improved about the guessing task?")
    # other
    feedback_other = models.LongStringField(doc='Additional feedback',
                                            label="Do you have any other additional feedback?")
    feedback_exp_demand = models.LongStringField(doc='Intention of study',
                                                 label="What do you think this study is trying to find?")


# PAGES
class Feedback(Page):
    form_model = 'player'
    form_fields = [
        'instructions_clear',
        'instructions_improve',
        'task_clear',
        'task_interesting',
        'task_difficult',
        'task_improve',
        'feedback_other',
        'feedback_exp_demand'
    ]


class End(Page):
    pass


page_sequence = [Feedback, End]
