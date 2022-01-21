from os import environ

SESSION_CONFIGS = [
    dict(
        name='belief_survey',
        display_name='Survey on Belief Updating',
        app_sequence=['Intro', 'belief_survey', 'questionnaire'],
        num_demo_participants=40,
    ),
]


# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=2.50, doc=""
)

PARTICIPANT_FIELDS = ['signals',
                      'ball',
                      'ball_extra',
                      'prev_verifications',
                      'verification_balls',
                      'verification_rounds',
                      'belief_q']
SESSION_FIELDS = []

# ISO-639 code
LANGUAGE_CODE = 'en'

REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = False

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '7277142838663'
