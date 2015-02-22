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
    * Outer loop - populate tweet queue 
    * Inner loop - tweet from tweet queue
    """
    def __init__(self,json_file):
        pass

    def perform_action(self,action,**kwargs):
        if action=='dummy':
            self.dummy(**kwargs)
        elif action=='echo':
            self.echo(**kwargs)

    def dummy(self,**kwargs):
        pass

    def echo(self,**kwargs):
        print "Hello world!"




    def populate_queue(self):
        pass

