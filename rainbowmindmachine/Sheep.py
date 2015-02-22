import twitter
import time
import simplejson as json
from numpy.random import rand


class Sheep(object):
    """
    App object (dict) to manage app info
    Account object (dict) to manage account info

    The bot performs two kinds of actions:
    1. Tweeting (real or fake)
    2. Non-tweeting

    Bot tweeting is a multi-layered action:
    * Outer loop - structure/prepare for/assemble tweets
    * Inner loop - actually tweet

    perform_action()
    """


