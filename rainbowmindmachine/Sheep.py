import urllib
import twitter
import time
import simplejson as json
import datetime
import traceback
from collections import deque
import base64

# Note:
# when ready to get to uploading media,
# see https://github.com/twitterdev/large-video-upload-python/blob/master/async-upload.py#L60
# (yuck)

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
    def __init__(self, json_file, lumberjack, **kwargs):
        """
        A Sheep object manages information for a single Twitter account.

        This information consists of public/private keys,
        and is contained in a json file (passed into the constructor).

        This info is used to create a Twitter API instance.

        **kwargs should include any information or parameters
        that are unique to the Sheep and that it should remember.
        """
        # This is where we should initialize the Twitter API instance 
        # using params found in the json file.
        with open(json_file,'r') as f:
            self.params = json.load(f)

        self.twitter_api_init()

        self.params = kwargs

        self.lumberjack = lumberjack


    def twitter_api_init(self):
        """
        This uses Json file (loaded into self.params)
        to construct a Twitter API instance.
        
        This is what the bot uses to tweet, 
        change its bio, etc.

        Uses bear's python-twitter library from Github
        (official version of what was the Google Code python-twitter):
        https://github.com/bear/python-twitter

        (bear's twitter api library gave some problems 
        when tweeting with attached media - may use a different 
        twitter library...)

        TODO: follow up on this
        """
        self.api = twitter.Api( consumer_key        = self.params['consumer_token'],
                                consumer_secret     = self.params['consumer_token_secret'],
                                access_token_key    = self.params['oauth_token'],
                                access_token_secret = self.params['oauth_token_secret'])
        msg = self.timestamp_message("Set up Twitter API for bot "+self.params['screen_name'])
        self.lumberjack.info(msg)


    def perform_action(self,action,params):
        """
        Performs action indicated by string action,
        passing a dictionary of parameters.

        Available actions:
        - dummy
        - echo
        - change_url
        - change_bio
        - change_color
        - change_image
        - tweet
        - follow_user
        - unfollow_user
        """
        if hasattr( self, action ):
            method = getattr( self, action )
            method( params )



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
        print("Hello world!")


    def change_url(self,params):
        """
        Update twitter profile url 

        Parameters:
        url         The url string for the API endpoint

        Does not return anything
        """
        if( 'url' not in params.keys()):
            # what are you doing??
            raise Exception("change_url() action called without 'url' key specified in the parameters dict.")

        bot_url = params['url']

        # Set the API endpoint 
        api_url = "https://api.twitter.com/1.1/account/update_profile.json"

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
        
        self.lumberjack.log(content)



    def change_bio(self,params):
        """
        Update twitter profile bio

        Parameters:
        bio         The bio string

        Does not return anything
        """
        if( 'bio' not in params.keys()):
            # what are you doing??
            raise Exception("change_bio() action called without 'bio' key specified in the parameters dict.")

        bot_bio = params['bio']

        handle = self.params['screen_name']

        # -----------------------------------------
        # Set the API endpoint 
        url = "https://api.twitter.com/1.1/account/update_profile.json"

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
        
        self.lumberjack.log(content)


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
        if( 'background' not in params.keys() and 'links' not in params.keys()):
            # what are you doing??
            raise Exception("change_color() action called without 'background' or 'links' keys specified in the parameters dict.")

        # json sent to the Twitter API
        payload = {}

        if 'background' in params.keys():
            background_rgbcode = params['background']
            payload['profile_background_color'] = background_rgbcode

        if 'links' in params.keys():
            links_rgbcode = params['links']
            payload['profile_link_color'] = links_rgbcode

        handle = self.params['screen_name']

        # Set the API endpoint 
        url = "https://api.twitter.com/1.1/account/update_profile_colors.json"

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
        
        self.lumberjack.log(content)



    def change_image(self,params):
        """
        Change a user's avatar image.

        Parameters:
        image       The path to the image to include

        (Note that unlike most actions, 
        the parameter passed in by the user
        must be pre-processed first.)

        This method does not return anything
        """
        # json sent to the Twitter API
        payload = {}

        if 'image' not in params.keys():
            # what are you doing?
            raise Exception("change_image() action called without an 'image' key specified in the params dict.")
        elif os.path.isfile(params['image']) is False:
            raise Exception("change_image() action called with 'image' key of params dict pointing to a non-existent file.")
        else: 
            img_file = params['image']
            b64 = base64.encodestring(open(img_file,"rb").read())

        # Set the API endpoint 
        api_url = "https://api.twitter.com/1.1/account/update_profile_image.json"

        token = oauth.Token(key = self.params['oauth_token'], 
                         secret = self.params['oauth_token_secret'])
        consumer = oauth.Consumer(key = self.params['consumer_token'], 
                               secret = self.params['consumer_token_secret'])
        client = oauth.Client(consumer,token)
        resp, content = client.request(
                api_url,
                method = "POST",
                body=urllib.urlencode({'image': b64}),
                headers=None
                )
        
        self.lumberjack.log(content)



    def follow_user(self, params, notify=True):
        """
        Follow a twitter user

        Parameters:
        username        The username of the user to follow
        notify          Whether to notify the followed user (boolean)

        This method does not return anything
        """
        # json sent to the Twitter API
        payload = {}

        if 'username' not in params.keys():
            # what are you doing?
            raise Exception("follow_user() action called without a 'username' key specified in the params dict.")
        else: 
            payload['user_id'] = params['username']

        # Set the API endpoint 
        url = "https://api.twitter.com/1.1/friendships/create.json"

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
        
        self.lumberjack.log(content)


    def unfollow_user(self, params, notify=True):
        """
        Unfollow a twitter user

        Parameters:
        username        The username of the user to unfollow

        This method does not return anything
        """
        # json sent to the Twitter API
        payload = {}

        if 'username' not in params.keys():
            # what are you doing?
            raise Exception("unfollow_user() action called without a 'username' key specified in the params dict.")
        else: 
            payload['user_id'] = params['username']

        # Set the API endpoint 
        url = "https://api.twitter.com/1.1/friendships/destroy.json"

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
        
        self.lumberjack.log(content)





    def populate_queue(self):
        """
        populate_queue() handles content.

        This method should be extended by new Sheep classes that have their own creative means of generating tweets.

        The default Sheep object will generate a tweet queue filled with 5 "Hello World" messages.
        """
        maxlen = 5
        tweet_queue = deque(maxlen=maxlen)
        
        for j in range(maxlen):

            tweet = "Hello world! That's number %d of 5."%(j+1)

            tweet_queue.extend([tweet])

        msg = self.timestamp_message("Finished populating a new tweet queue with %d tweets."%(len(tweet_queue)))
        self.lumberjack.log(msg)

        return tweet_queue



    def tweet(self,params):
        """
        tweet() handles scheduling.

        Run an infinity loop in which the bot decides when to tweet.

        Default Sheep have the following scheduling parameters:
        
            inner_sleep         Inner loop sleep time (1 s)
            outer_sleep         Outer loop sleep time (10 s)
            publish             Actually publish (False)

        Not sure if we need this keyword:

            tweet_metadata      Tweet metadata ({})

        This function never ends, so it never returns.
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
        #
        # call populate_queue() to populate the list of tweets to send out
        # 
        # apply some rube goldberg logic to figure out when to tweet each item

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
                self.lumberjack.log(msg)


            except Exception:

                # oops!

                msg1 = self.timestamp_message("Sheep encountered an exception. More info:")
                msg2 = self.timestamp_message(traceback.format_exc())
                msg3 = self.timestamp_message("Sheep is continuing...")

                self.lumberjack.log(msg1)
                self.lumberjack.log(msg2)
                self.lumberjack.log(msg3)

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
                self.lumberjack.log(msg)

        except twitter.TwitterError as e:
            
            if e.message[0]['code'] == 185:
                msg = self.timestamp_message("Twitter error: Daily message limit reached")
                self.lumberjack.log(msg)

            elif e.message[0]['code'] == 187:
                msg = self.timestamp_message("Twitter error: Duplicate error")
                self.lumberjack.log(msg)
            
            else:
                msg = self.timestamp_message("Twitter error: "+e.message)
                self.lumberjack.log(msg)


        ## DEBUG
        #self._print(twit)
        ## END DEBUG



    def _print(self,twit):
        """
        Private method.
        Print a twit.
        """
        msg = self.timestamp_message("> "+twit)
        self.lumberjack.log(msg)


    def timestamp_message(self,message):
        """
        Add a timestamp and a user handle to a message for logging purposes.
        """
        result = "[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " @" + self.params['screen_name']+"] " + message
        return result

