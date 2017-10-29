FORMATTER = 'formatters.LadderFormatter'

DELAY = 0.4

BANNED_WORDS = [
    'importlib._bootstr',
    '/usr/lib/python3',
]


# set your own settings which shouldn't affect the project
# in local_settings.py
try:
    from local_settings import *
except ImportError:
    pass
