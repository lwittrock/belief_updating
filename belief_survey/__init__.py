from otree.api import *
import random
import math

author = 'Lars Wittrock'

doc = """
This app presents participants with information and asks for probabilistic beliefs.
"""


class Constants(BaseConstants):
    # From Otree
    name_in_url = 'guessing_survey'
    players_per_group = None

    # Main inputs
    prob_urn = 0.75  # distribution of balls in relevant urn (i.e. 3/4 red balls in red urn and vice versa)
    prob_fake = 0.6  # distribution of balls in box (i.e. 6 out of 10 balls in box are uninformative)
    prob_box = 0.5  # distribution of non-urn balls (i.e. uninformative ball distribution 3-3)
    num_balls = 9  # number of balls shown - not including verifications
    verifications = [[2, 3, 4], [3, 4, 5], [4, 5, 6], [5, 6, 7], [6, 7, 8]]  # Balls to be verified.
    test_questions_solution = [1, 2, 3, 3, 3]  # Correct answers to the 4 test questions. TO UPDATE
    test_questions_required = 4  # Number of correct test questions required to proceed with experiment.
    scoring_rule_factor = 3

    # Implied inputs
    num_rounds = num_balls + len(verifications[0])


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Variables for instruction test
    test1 = models.IntegerField(doc='Test question 1',
                                label='1. What are the chances that the red urn is randomly selected?',
                                choices=[
                                    [1, '50%'],
                                    [2, '30%'],
                                    [3, '90%'],
                                    [4, '0%']
                                ],
                                widget=widgets.RadioSelect)
    test2 = models.IntegerField(doc='Test question 2',
                                label='2. How many balls in the black box are from the selected urn?',
                                choices=[
                                    [1, '2'],
                                    [2, '4'],
                                    [3, '6'],
                                    [4, '8']
                                ],
                                widget=widgets.RadioSelect)
    test3 = models.IntegerField(doc='Test question 3',
                                label='3. How many balls in the black box are NOT from the selected urn?',
                                choices=[
                                    [1, '2'],
                                    [2, '4'],
                                    [3, '6'],
                                    [4, '8']
                                ],
                                widget=widgets.RadioSelect)
    test4 = models.IntegerField(doc='Test question 3',
                                label='4. A blue ball is drawn from the black box. What does that mean?',
                                choices=[
                                    [1, 'The urn selected in the beginning is more likely to be red.'],
                                    [2, 'This does not tell me anything about the urn selected in the beginning.'],
                                    [3, 'The urn selected in the beginning is more likely to be blue.']
                                ],
                                widget=widgets.RadioSelect)
    test5 = models.IntegerField(doc='Test question 5',
                                label='5. You see a red ball with a question mark written on it. What does that mean?',
                                choices=[
                                    [1, 'It is unclear if the ball is red or blue.'],
                                    [2, 'The ball came from one of the uninformative ones'],
                                    [3, 'It is unclear if the ball is informative or uninformative.'],
                                    [4, 'The ball came from one of the informative ones.']
                                ],
                                widget=widgets.RadioSelect)

    test_correct = models.IntegerField(doc='Number of correct test questions')

    # Variables for urn, signals and belief input
    urn = models.IntegerField(doc='Randomly generated urn color, 0=blue and 1=red')
    ball = models.StringField(doc='Ball color shown')
    verification = models.StringField(doc='Fake/confirm signal')
    belief = models.IntegerField(doc='Reported belief p(R)')

    # Round variables
    verify_round = models.BooleanField(doc='True/false variable indicating verification rounds')
    pay_round = models.IntegerField(doc='Randomly chosen payoff round')

    # Variables for additional indep variables
    sr_button_clicks = models.IntegerField(doc='Number of times clicked tell me more button in instructions for scoring rule')
    info_button_clicks = models.IntegerField(doc='Number of times clicked background instruction button')


def creating_session(subsession: Subsession):
    # Calculating probabilities given the input parameters
    a = (Constants.prob_urn * (1 - Constants.prob_fake))  # inf. ball, correct color: 0.3
    b = ((1 - Constants.prob_urn) * (1 - Constants.prob_fake))  # inf. ball, incorrect color: 0.1
    c = (Constants.prob_box * Constants.prob_fake)  # uninf. ball, correct color: 0.3
    d = ((1 - Constants.prob_box) * Constants.prob_fake)  # uninf. ball, incorrect color: 0.3

    # red ball in round r - true or not
    def ball_red(r):
        if (player.in_round(r).urn == 1 and draw < a + c) or \
                (player.in_round(r).urn == 0 and draw < b + d):
            return True
        else:
            return False

    # All possible signals
    sig_blue = ["blue", '', 'img/blue_ball_q.png']
    sig_red = ["red", '', 'img/red_ball_q.png']
    sig_blue_true = ["blue", "true", 'img/blue_ball_i.png']
    sig_blue_fake = ["blue", "fake", 'img/blue_ball_u.png']
    sig_red_true = ["red", "true", 'img/red_ball_i.png']
    sig_red_fake = ["red", "fake", 'img/red_ball_u.png']

    # Randomizing urn and signals for each participant
    if subsession.round_number == 1:
        for player in subsession.get_players():

            # Define participant variables
            participant = player.participant
            participant.signals = []
            participant.ball = []
            participant.ball_extra = []

            # Randomize which balls are verified per player and create verification rounds vector
            participant.verification_balls = random.choice(Constants.verifications)
            participant.verification_rounds = []
            n = 0
            for element in participant.verification_balls:
                n += 1
                participant.verification_rounds.append(element + n)

            # Random pay round
            player.pay_round = random.randint(1, Constants.num_rounds)

            # Random urn draw - 50-50 chance
            player.urn = round(random.uniform(0, 1))  # 0: blue and 1: red

            # Generate signals each round, given the urn draw
            list_of_round_ids = range(1, Constants.num_rounds + 1)
            for i in list_of_round_ids:
                player.in_round(i).urn = player.in_round(1).urn
                player.in_round(i).pay_round = player.in_round(1).pay_round

                draw = random.uniform(0, 1)
                if i not in participant.verification_rounds:  # randomize blue / red given urn distribution and urn draw

                    if ball_red(i):
                        participant.signals.append(sig_red)
                        participant.ball.append(sig_red)
                    else:
                        participant.signals.append(sig_blue)
                        participant.ball.append(sig_blue)

                else:  # randomize true/fake and repeat ball from previous round (i-2 as list starts at element 0).

                    if participant.signals[i - 2][0] == 'red' and draw < Constants.prob_fake:
                        participant.signals.append(sig_red_fake)
                        participant.ball_extra.append(sig_red_fake)

                    elif participant.signals[i - 2][0] == 'red' and draw > Constants.prob_fake:
                        participant.signals.append(sig_red_true)
                        participant.ball_extra.append(sig_red_true)

                    elif participant.signals[i - 2][0] == 'blue' and draw < Constants.prob_fake:
                        participant.signals.append(sig_blue_fake)
                        participant.ball_extra.append(sig_blue_fake)

                    elif participant.signals[i - 2][0] == 'blue' and draw > Constants.prob_fake:
                        participant.signals.append(sig_blue_true)
                        participant.ball_extra.append(sig_blue_true)

            print(participant.verification_balls)  # to check
            print(participant.signals)

            # Creating vector of previous verifications - same length as participant.ball - used for ball display later
            participant.prev_verifications = []
            list_of_ball_ids = range(1, Constants.num_balls + 1)
            n = 0
            for i in list_of_ball_ids:
                participant.prev_verifications.append(n)
                if i in participant.verification_balls:
                    n += 1

    for player in subsession.get_players():

        # True/False variable if a given round is a verification round
        if player.round_number in player.participant.verification_rounds:
            player.verify_round = True
        else:
            player.verify_round = False


##########################################################################
# PAGES
##########################################################################

# Instructions and test are only shown in the beginning, i.e. in round 1
class Instructions(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

    form_model = 'player'
    form_fields = ['test1', 'test2', 'test3', 'test4', 'test5', 'sr_button_clicks']

    @staticmethod
    def vars_for_template(player: Player):
        def scoring_rule(belief, urn):
            if urn == 'red':
                error_red = (100-belief)/100
                score = Constants.scoring_rule_factor - Constants.scoring_rule_factor * math.pow(error_red, 2)
            else:
                error_blue = belief/100
                score = Constants.scoring_rule_factor - Constants.scoring_rule_factor * math.pow(error_blue, 2)
            return score

        example_60_red = scoring_rule(60, 'red')
        example_60_blue = scoring_rule(60, 'blue')

        return{
            'example_60_blue': example_60_blue,
            'example_60_red': example_60_red
        }

    # Correct answers for test questions
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.test1 == Constants.test_questions_solution[0]:
            test1_correct = 1
        else:
            test1_correct = 0

        if player.test2 == Constants.test_questions_solution[1]:
            test2_correct = 1
        else:
            test2_correct = 0

        if player.test3 == Constants.test_questions_solution[2]:
            test3_correct = 1
        else:
            test3_correct = 0

        if player.test4 == Constants.test_questions_solution[3]:
            test4_correct = 1
        else:
            test4_correct = 0

        if player.test5 == Constants.test_questions_solution[4]:
            test5_correct = 1
        else:
            test5_correct = 0

        player.test_correct = test1_correct + test2_correct + test3_correct + test4_correct + test5_correct


class InstructionsFeedback(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1


class UrnDraw(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1


class BeliefInput(Page):
    form_model = 'player'
    form_fields = ['belief', 'info_button_clicks']

    @staticmethod
    def vars_for_template(player: Player):
        # defining which ball is displayed -
        def pic_displayed(i):
            if player.round_number >= i + player.participant.prev_verifications[i - 1]:
                if i not in player.participant.verification_balls:
                    pic = player.participant.ball[i - 1][2]
                else:
                    if player.round_number > i + player.participant.prev_verifications[i - 1]:
                        pic = player.participant.ball_extra[player.participant.prev_verifications[i - 1]][
                            2]  # ... = number of previous verification rounds
                    else:
                        pic = player.participant.ball[i - 1][2]
            else:
                pic = 'img/blank_png.png'
            return pic

        # writing signals to data set
        player.ball = player.participant.signals[player.round_number - 1][0]
        player.verification = player.participant.signals[player.round_number - 1][1]

        prev_ball = ''
        if player.round_number > 1:
            prev_ball = player.participant.signals[player.round_number - 2][0]

        # if round is equal to ball verified. then first show ball and in rounds >= round + 1 show the other ball

        pic1 = pic_displayed(1)
        pic2 = pic_displayed(2)
        pic3 = pic_displayed(3)
        pic4 = pic_displayed(4)
        pic5 = pic_displayed(5)
        pic6 = pic_displayed(6)
        pic7 = pic_displayed(7)
        pic8 = pic_displayed(8)
        pic9 = pic_displayed(9)

        # Return generated variables, used for display of information
        return {
            'pic1': pic1,
            'pic2': pic2,
            'pic3': pic3,
            'pic4': pic4,
            'pic5': pic5,
            'pic6': pic6,
            'pic7': pic7,
            'pic8': pic8,
            'pic9': pic9,

            'prev_ball': prev_ball,
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.round_number == player.pay_round:
            if player.urn == 0:
                player.payoff = Constants.scoring_rule_factor - \
                                Constants.scoring_rule_factor * math.pow(player.belief/100, 2)
            else:
                player.payoff = Constants.scoring_rule_factor - \
                                Constants.scoring_rule_factor * math.pow(1-player.belief/100, 2)
        else:
            player.payoff = 0


# Sequence of pages to be displayed
page_sequence = [Instructions,
                 InstructionsFeedback,
                 UrnDraw,
                 BeliefInput
                 ]
