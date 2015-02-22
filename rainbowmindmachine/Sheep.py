import twitter
import time
import simplejson as json
import datetime
from numpy.random import rand
from collections import deque

from Lumberjack import *


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
        """
        Sheep own information pertaining to a Twitter account.
        This information consists of public/private keys,
        and is contained in the Json file.
        This info is used to create a Twitter API instance.
        """

        # this is where we should 
        # initialize the Twitter 
        # API instance using params
        # found in the json file.
        with open(json_file,'r') as f:
            self.params = json.load(f)

        self.twitter_api_init()


    def twitter_api_init(self):
        """
        This uses Json file (loaded into self.params)
        to construct a Twitter API instance.
        
        This is what the bot uses to tweet, 
        change its bio, etc.

        While I have been using Bear's Twitter API library,
        I had problems using it for tweets with media attached,
        so I switched to a different library. I forget which one.

        (check Flickr photobots for which library works for media posts...)
        """
        pass


    def perform_action(self,action,params):
        """
        Performs action indicated by string action,
        passing a dictionary of parameters params
        """

        if action=='dummy':
            self.dummy(params)

        elif action=='echo':
            self.echo(params)

        elif action=='tweet':
            self.tweet(params)


    def dummy(self,params):
        """
        Debug:
        Do nothing
        """
        pass


    def echo(self,params):
        """
        Just say hi
        """
        print "Hello world!"


    def tweet(self,params):
        """
        Keyword arguments:

        inner_sleep     Inner loop sleep time (1 s)
        outer_sleep     Outer loop sleep time (10 s)
        publish         Actually publish (False)

        Not sure if we need this keyword:

        tweet_metadata  Tweet metadata ({})
        """

        # --------------------------
        # Process parameters

        tweet_params = params

        # Default parameter values
        defaults = {}
        defaults['inner_sleep'] = 1.0
        defaults['outer_sleep'] = 10.0
        defaults['publish'] = False
        #defaults['tweet_metadata'] = {}

        # populate missing params with default values
        for dk in defaults.keys():
            if dk not in tweet_params.keys():
                tweet_params[dk] = defaults[dk]

        # --------------------------
        # The Real McCoy

        while True:

            try:
                
                # Outer loop
                tweet_queue = self.populate_queue()

                for ii in range(len(tweet_queue)):

                    twit = tweet_queue.popleft()

                    # Fire off the tweet
                    if tweet_params['publish']:
                        self._tweet( twit )
                    else:
                        self._print( twit )


                    time.sleep( tweet_params['inner_sleep'] )


                time.sleep( tweet_params['outer_sleep'] )

                msg = self.timestamp_message("Completed a cycle.")


            except:
                # TODO
                # add more info about exception
                # oops!
                msg = self.timestamp_message("Encountered an exception. Continuing...")
                logging.info(msg)

                time.sleep( tweet_params['outer_sleep'] )




    def _tweet(self,twit):
        """
        Private method.
        Publish a twit.
        """
        self._print(twit)



    def _print(self,twit):
        """
        Private method.
        Print a twit.
        """
        msg = self.timestamp_message(twit)
        logging.info(msg)

        print "+"*20
        print msg
        print "+"*20
        print "\n"


    def populate_queue(self):
        """
        This method is extended/defined by derived Sheep.

        Default Sheep still generate a dummy tweet queue
        """
        maxlen = 5
        tweet_queue = deque(maxlen=maxlen)
        
        for j in range(maxlen):

            tweet = "Hello world! That's number %d of 5."%(j+1)

            tweet_queue.extend([tweet])

        msg = self.timestamp_message("Finished populating a new tweet queue with %d tweets."%(len(tweet_queue)))
        logging.info(msg)

        return tweet_queue



    def timestamp_message(self,message):

        # We don't actually need to timestamp our messages,
        # since logging will do that for us.
        # So just sign with twitter handle.

        #result = "[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " @" + self.params['screen_name']+"] " + message

        result = "[@" + self.params['screen_name']+"] " + message

        return result

