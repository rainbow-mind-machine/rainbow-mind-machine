import twitter
import time
import simplejson as json
import datetime
import logging
from numpy.random import rand
from collections import deque


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

        Uses bear's python-twitter library from Github
        (official version of what was the Google Code python-twitter):
        https://github.com/bear/python-twitter

        While I have been using Bear's Twitter API library,
        I had problems using it for tweets with media attached,
        so for those, switch to a different library. 
        I forget which one.

        (check Flickr photobots for which library works for media posts...)
        """
        self.api = twitter.Api( consumer_key        = self.params['consumer_token'],
                                consumer_secret     = self.params['consumer_token_secret'],
                                access_token_key    = self.params['oauth_token'],
                                access_token_secret = self.params['oauth_token_secret'])
        msg = self.timestamp_message("Set up Twitter API for bot "+self.params['screen_name'])
        logging.info(msg)


    def perform_action(self,action,params):
        """
        Performs action indicated by string action,
        passing a dictionary of parameters params
        """

        if action=='dummy':
            self.dummy(params)

        elif action=='echo':
            self.echo(params)

        elif action=='change url':
            self.change_url(params)

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


    def change_url(self,params):
        """
        Update bio to have a different URL
        """
        # Set the API endpoint 
        url = "https://api.twitter.com/1.1/account/update_profile.json"

        import urllib

        token = oauth.Token(key = self.params['oauth_token'], 
                         secret = self.params['oauth_token_secret'])
        consumer = oauth.Consumer(key = self.params['consumer_token'], 
                               secret = self.params['consumer_token_secret'])
        client = oauth.Client(consumer,token)
        resp, content = client.request(
                url,
                method = "POST",
                body=urllib.urlencode({'url': bot_url}),
                headers=None
                )
        
        print content


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
                logging.info(msg)


            except Exception as inst:
                # TODO
                # add more info about exception
                # oops!

                msg = self.timestamp_message("Sheep encountered an exception. More info:")
                logging.info(msg)

                msg2 = self.timestamp_message(str(inst))
                logging.info(msg2)

                msg3 = self.timestamp_message("Sheep is continuing...")
                logging.info(msg3)

                time.sleep( tweet_params['outer_sleep'] )




    def _tweet(self,twit):
        """
        Private method.
        Publish a twit.
        """
        # call twitter api to tweet twit
        # (until then, just print)
        self._print(twit)



    def _print(self,twit):
        """
        Private method.
        Print a twit.
        """
        msg = self.timestamp_message("> "+twit)
        logging.info(msg)


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

