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

        # this is where we should 
        # initialize the Twitter 
        # API instance using params
        # found in the json file.
        with open(json_file,'r') as f:
            self.params = json.load(f)

        self.twitter_api_init()


    def twitter_api_init(self):
        # use self.params
        # (also check Flickr photobots
        #  for which library works for
        #  media posts...)
        pass


    def perform_action(self,action,**kwargs):

        if action=='dummy':
            self.dummy(**kwargs)

        elif action=='echo':
            self.echo(**kwargs)

        elif action=='tweet':
            self.tweet(**kwargs)


    def dummy(self,**kwargs):
        pass


    def echo(self,**kwargs):
        print "Hello world!"


    def tweet(self,**kwargs):
        """
        Keyword arguments:

        inner_sleep     Inner loop sleep time (1 s)
        outer_sleep     Outer loop sleep time (10 s)
        publish         Actually publish (False)
        """

        # --------------------------
        # Process parameters

        tweet_params = kwargs

        # Default parameter values
        defaults['inner_sleep'] = 1.0
        defaults['outer_sleep'] = 10.0
        defaults['publish'] = False

        # populate missing params with default values
        for dk in defaults.keys():
            if dk not in kwargs.keys():
                tweet_params[dk] = defaults[dk]

        # --------------------------
        # The Real McCoy

        while True:

            try:
                
                # Outer loop
                twitter_queue = self.populate_queue()

                for tweet in twitter_queue:


            pass:
                # oops!
                print "Encountered an exception. Continuing..."
                time.sleep(


    def populate_queue(self):
        pass


