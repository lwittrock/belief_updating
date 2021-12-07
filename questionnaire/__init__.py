from otree.api import *
import pytz

author = 'Lars Wittrock'

doc = """
Post experiment survey - meant after belief survey.
"""


class Constants(BaseConstants):
    name_in_url = 'questionnaire'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Belief Questions TO ADD MORE HERE
    open_feedback = models.LongStringField(doc='Open ended description of what a subject did and why.')
    belief_optimal = models.IntegerField(doc='Subjective probability regarding optimality of own action',
                                         label='In theory, for each ball that was shown to you it was possible to calculate '
                                               'the exact percentage chance the selected urn was red. '
                                               'How close (in percentage points) do you think you were on average to this correct probability?')
    belief_fake_blue = models.IntegerField(doc='Subjective probability blue signals are fake',
                                           label='How likely is it that blue balls were fake?')
    belief_fake_red = models.IntegerField(doc='Subjective probability red signals are fake',
                                          label='How likely is it that red balls were fake?')

    # CRT
    crt1 = models.IntegerField(doc='CRT1 - Running',
                               label='1. If you are running a race and you pass the person in second place, what place are you in?',
                               choices=[
                                   [1, 'First.'],
                                   [2, 'Second.'],
                                   [3, 'Third.'],
                                   [4, 'Not enough information.']
                               ],
                               widget=widgets.RadioSelect)
    crt2 = models.IntegerField(doc='CRT2 - ',
                               label='2. A farmer had 15 sheep and all but 8 died. How many are left?',
                               choices=[
                                   [1, '15.'],
                                   [2, '8.'],
                                   [3, '7.'],
                                   [4, 'Not enough information.']
                               ],
                               widget=widgets.RadioSelect)
    crt3 = models.IntegerField(doc='CRT3 - ',
                               label="3. Emily's father has three daughters. The first two are named April and May. What is the third daughter's name?",
                               choices=[
                                   [1, 'June.'],
                                   [2, 'July.'],
                                   [3, 'Emily.'],
                                   [4, 'Not enough information.']
                               ],
                               widget=widgets.RadioSelect)
    crt4 = models.IntegerField(doc='CRT4 - lethal heart attacks',
                               label='4. How many lethal heart attacks did you survive this far?',
                               choices=[
                                   [1, 'Zero.'],
                                   [2, '1.'],
                                   [3, '2.'],
                                   [4, '3 or more.']
                               ],
                               widget=widgets.RadioSelect)
    # Demographics
    age = models.IntegerField(doc='Age',
                              label='How old are you?',
                              min=16,
                              max=100)
    gender = models.IntegerField(doc='Gender',
                                 label='What is your gender?',
                                 choices=[
                                     [1, 'Female'],
                                     [2, 'Male'],
                                     [3, 'Other']
                                 ])
    edu = models.IntegerField(doc='Level of educations',
                              label='What is the highest level of education you have completed?',
                              choices=[
                                  [1, 'No completed education.'],
                                  [2, 'High school'],
                                  [3, 'Bachelor or equivalent'],
                                  [4, 'Master or equivalent'],
                                  [5, 'PhD'],
                                  [6, 'Other']
                              ])
    occ = models.IntegerField(doc='Occupations',
                              label='What best describes your main occupation at this moment?',
                              choices=[
                                  [1, 'Student'],
                                  [2, 'Unemployed'],
                                  [3, 'Working part time'],
                                  [4, 'Working full time'],
                                  [5, 'Other']
                              ])
    country = models.StringField(doc='Country of residence',
                                 label='What is your country of residence?',
                                 choices=pytz.country_names.items()
                                 )
    prob_fam = models.IntegerField(doc='Level of familiarity with probabilities',
                                   label='How familiar would you describe yourself with probabilities?',
                                   choices=[
                                       [1, 'I have no idea about it.'],
                                       [2, 'I have heard of it, but I do not know much about it.'],
                                       [3, 'I know a bit about it.'],
                                       [4, 'I understand it well.']
                                   ])


# PAGES
class Transition(Page):
    pass


class BeliefQuestions(Page):
    form_model = 'player'
    form_fields = ['open_feedback', 'belief_optimal', 'belief_fake_blue', 'belief_fake_red']

    def vars_for_template(player: Player):
        belief_q_label = 'We would like to hear your thoughts on the choices you made. ' \
                         'To do so we will take one round you saw during the study. In round ' \
                         + str(player.participant.belief_q[0]) + \
                         ' you saw a ' \
                         + str(player.participant.belief_q[1]) + \
                         ' ball and reported ' \
                         + str(player.participant.belief_q[2]) + \
                         '% probability. In the next round you learnt that the previously drawn ball was ' \
                         + str(player.participant.belief_q[4]) + \
                         '. You then reported ' \
                         + str(player.participant.belief_q[5]) + \
                         '%. What were your thoughts for making that report?'

        return {'belief_q_label': belief_q_label}

class CRT(Page):
    form_model = 'player'
    form_fields = ['crt1', 'crt2', 'crt3', 'crt4']


class Demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'edu', 'occ', 'country', 'prob_fam']


class FinalPage(Page):
    # feedback on correct urn and payment.
    pass


page_sequence = [Transition, BeliefQuestions, CRT, Demographics, FinalPage]
