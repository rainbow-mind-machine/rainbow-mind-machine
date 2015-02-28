import twitter
import time
import simplejson as json
import datetime
import logging
import traceback
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

        elif action=='change bio':
            self.change_bio(params)

        elif action=='change color':
            self.change_color(params)

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
        Update twitter profile url 

        Parameters:
        url         The url string

        Does not return anything
        """
        bot_url = params['url']

        # Set the API endpoint 
        api_url = "https://api.twitter.com/1.1/account/update_profile.json"

        import urllib

        token = oauth.Token(key = self.params['oauth_token'], 
                         secret = self.params['oauth_token_secret'])
        consumer = oauth.Consumer(key = self.params['consumer_token'], 
                               secret = self.params['consumer_token_secret'])
        client = oauth.Client(consumer,token)
        resp, content = client.request(
                api_url,
                method = "POST",
                body=urllib.urlencode({'url': bot_url}),
                headers=None
                )
        
        print content



    def change_bio(self,params):
        """
        Update twitter profile bio

        Parameters:
        bio         The bio string

        Does not return anything
        """
        bot_bio = params['bio']

        handle = self.params['screen_name']

        # -----------------------------------------
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
                body=urllib.urlencode({'description': bot_bio}),
                headers=None
                )
        
        print content


    def change_color(self,params):
        """
        Update twitter profile colors

        Parameters:
        background      RGB code for background color (no #)
        links           RGB code for links color (no #)
        
        Example:
        params = {'background':'3D3D3D', 'link':'AAF'}

        Does not return anything
        """

        # Json sent to the Twitter API
        payload = {}

        if 'background' in params.keys():
            background_rgbcode = params['background']
            payload['profile_background_color'] = background_rgbcode

        if 'links' in params.keys():
            links_rgbcode = params['links']
            payload['profile_link_color'] = links_rgbcode

        handle = self.params['screen_name']


        # -----------------------------------------
        # Set the API endpoint 
        url = "https://api.twitter.com/1.1/account/update_profile_colors.json"

        import urllib

        token = oauth.Token(key = self.params['oauth_token'], 
                         secret = self.params['oauth_token_secret'])
        consumer = oauth.Consumer(key = self.params['consumer_token'], 
                               secret = self.params['consumer_token_secret'])
        client = oauth.Client(consumer,token)
        resp, content = client.request(
                url,
                method = "POST",
                body=urllib.urlencode(payload),
                headers=None
                )
        
        print content





    def tweet(self,params):
        """
        Tweets forever.

        Parameters:
        inner_sleep     Inner loop sleep time (1 s)
        outer_sleep     Outer loop sleep time (10 s)
        publish         Actually publish (False)

        Not sure if we need this keyword:
        tweet_metadata  Tweet metadata ({})

        Never returns, because never ends.
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

                assert (len(tweet_queue)>0)

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


            except Exception,err:

                # oops!

                msg1 = self.timestamp_message("Sheep encountered an exception. More info:")
                msg2 = self.timestamp_message(traceback.format_exc())
                msg3 = self.timestamp_message("Sheep is continuing...")

                logging.info(msg1)
                logging.info(msg2)
                logging.info(msg3)

                time.sleep( tweet_params['outer_sleep'] )

            except AssertionError:
                raise Exception("Error: tweet queue was empty. Check your populate_queue() method definition.")



    def _tweet(self,twit):
        """
        Private method.
        Publish a twit.
        """
        # call twitter api to tweet the twit

        try:
            # tweet:
            stats = self.api.PostUpdates(twit)

            # everything else:
            for stat in stats:
                msg = self.timestamp_message(">>> "+twit)
                logging.info(msg)

        except twitter.TwitterError as e:
            
            if e.message[0]['code'] == 185:
                msg = self.timestamp_message("Twitter error: Daily message limit reached")
                logging.info(msg)

            elif e.message[0]['code'] == 187:
                msg = self.timestamp_message("Twitter error: Duplicate error")
                logging.info(msg)
            
            else:
                msg = self.timestamp_message("Twitter error: "+e.message)
                logging.info(msg)


        ## DEBUG
        #self._print(twit)
        ## END DEBUG



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

