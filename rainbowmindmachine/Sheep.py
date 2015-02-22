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
        tweet_metadata  Tweet metadata ({})
        """

        # --------------------------
        # Process parameters

        tweet_params = kwargs

        # Default parameter values
        defaults['inner_sleep'] = 1.0
        defaults['outer_sleep'] = 10.0
        defaults['publish'] = False
        defaults['tweet_metadata'] = {}

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

                for twit in twitter_queue:

                    #self.publish()
                    if tweet_params['publish']:
                        self._tweet( twit, tweet_params['tweet_metadata'] )
                    else:
                        self._print( twit, tweet_params['tweet_metadata'] )

                    time.sleep( tweet_params['inner_sleep'] )

                time.sleep( tweet_params['outer_sleep'] )

            except:
                # oops!
                print "Encountered an exception. Continuing..."
                time.sleep( tweet_params['outer_sleep'] )


    def populate_queue(self):
        print "*"*40
        print "WARNING: You called populate_queue on the parent Sheep method."
        print "         You must extend Sheep and define populate_queue() "
        print "         in the child class."


    def _tweet(self,twit,metadata):
        self._print(twit,metada)

    def _print(self,twit,metadata):
        print "\n"
        print "+"*20
        print "Tweet:",twit
        print "Metadata:",metadata
        print "+"*20
        print "\n"





