import urllib
import oauth2 as oauth
import twitter
import time
import logging
import simplejson as json
import datetime
import traceback
from collections import deque
import base64

"""
Sheep
"""

class Sheep(object):
    """
    - input bot key (JSON file) is stored as self.params and contains everything the sheep needs
    - by default, bot tweeting is two-layered:
        - outer loop populates tweet queue
        - inner loop tweets from the tweet queue
    """
    def __init__(self, json_file, **kwargs):
        """
        json_file - parameters that come from the keys (and the Keymaker, and the key-making process)

        kwargs - extra parameter args passed into the Sheep from the Shepherd

        A Sheep object manages information for a single Twitter bot account.
        The information (oauth keys, bot name, bot account, etc) are contained
        in the JSON file passed in by the Shepherd.

        The JSON file contains information compiled by the Keymaker.
        If there is other information the Shepherd needs to pass to the 
        Sheep that is not in the JSON file, it can use keyword args.
        """
        # This is where we should initialize the Twitter API instance 
        # using params found in the json file.
        with open(json_file,'r') as f:
            self.params = json.load(f)

        self.twitter_api_init()

        # combine the user-provided parameters 
        # (in kwargs) with the json-provided parameters
        for keys in kwargs:
            self.params[key] = kwargs[key]


    def twitter_api_init(self):
        """
        This uses json input file (loaded into self.params)
        to construct a Twitter API instance.
        
        This is what the bot uses to tweet, 
        change its bio, etc.

        Uses bear's python-twitter library from Github
        (official version of what was the Google Code python-twitter):
        https://github.com/bear/python-twitter
        """
        self.api = twitter.Api( consumer_key        = self.params['consumer_token'],
                                consumer_secret     = self.params['consumer_token_secret'],
                                access_token_key    = self.params['oauth_token'],
                                access_token_secret = self.params['oauth_token_secret'])

        logger = logging.getLogger('rainbowmindmachine')
        msg = self.timestamp_message("Set up Twitter API for bot "+self.params['screen_name'])
        logger.info(msg)


    def perform_action(self,action,extra_params):
        """
        Performs action indicated by string action,
        passing a dictionary of extra parameters.

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
        # Use the dispatcher method pattern
        if hasattr( self, action ):
            method = getattr( self, action )
            method( extra_params )



    def dummy(self,extra_params):
        """
        Debug:
        Do nothing
        """
        pass


    def echo(self,extra_params):
        """
        Just say hi
        """
        print("Hello world!")


    def change_url(self,extra_params):
        """
        Update twitter profile url 

        Parameters:
        url         The url string for the API endpoint

        Does not return anything
        """
        logger = logging.getLogger('rainbowmindmachine')

        if( 'url' not in extra_params.keys()):
            err = "change_url() action called without 'url' key specified in the parameters dict."
            logger.error(err)
            raise Exception(err)

        bot_url = extra_params['url']

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
        
        logger.info(content)



    def change_bio(self,extra_params):
        """
        Update twitter profile bio

        Parameters:
        bio         The bio string

        Does not return anything
        """
        logger = logging.getLogger('rainbowmindmachine')

        if( 'bio' not in extra_params.keys()):
            err = "change_bio() action called without 'bio' key specified in the parameters dict."
            logger.error(err)
            raise Exception(err)

        bot_bio = extra_params['bio']

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
        
        logger.info(content)


    def change_color(self,extra_params):
        """
        Update twitter profile colors

        Parameters:
        background      RGB code for background color (no #)
        links           RGB code for links color (no #)
        
        Example:
        extra_params = {'background':'3D3D3D', 'link':'AAF'}

        Does not return anything
        """
        logger = logging.getLogger('rainbowmindmachine')

        if( 'background' not in extra_params.keys() and 'links' not in extra_params.keys()):
            err = "change_color() action called without 'background' or 'links' keys specified in the parameters dict."
            logger.error(err)
            raise Exception(err)

        # json sent to the Twitter API
        payload = {}

        if 'background' in extra_params.keys():
            background_rgbcode = extra_params['background']
            payload['profile_background_color'] = background_rgbcode

        if 'links' in extra_params.keys():
            links_rgbcode = extra_params['links']
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
        
        logger.info(content)



    def change_image(self,extra_params):
        """
        Change a user's avatar image.

        Parameters:
        image       The path to the image to include

        (Note that unlike most actions, 
        the parameter passed in by the user
        must be pre-processed first.)

        This method does not return anything
        """
        logger = logging.getLogger('rainbowmindmachine')

        # json sent to the Twitter API
        payload = {}

        if 'image' not in extra_params.keys():
            err = "change_image() action called without an 'image' key specified in the params dict."
            logger.error(err)
            raise Exception(err)
        elif os.path.isfile(extra_params['image']) is False:
            err = "change_image() action called with 'image' key of params dict pointing to a non-existent file."
            logger.error(err)
            raise Exception(err)
        else: 
            img_file = extra_params['image']
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
        
        logger.info(content)



    def follow_user(self, extra_params, notify=True):
        """
        Follow a twitter user

        Parameters:
        username        The username of the user to follow
        notify          Whether to notify the followed user (boolean)

        This method does not return anything
        """
        logger = logging.getLogger('rainbowmindmachine')

        # json sent to the Twitter API
        payload = {}

        if 'username' not in extra_params.keys():
            err = "follow_user() action called without a 'username' key specified in the params dict."
            logger.error(err)
            raise Exception(err)
        else: 
            payload['user_id'] = extra_params['username']

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
        
        logger.info(content)


    def unfollow_user(self, extra_params, notify=True):
        """
        Unfollow a twitter user

        Parameters:
        username        The username of the user to unfollow

        This method does not return anything
        """
        logger = logging.getLogger('rainbowmindmachine')

        # json sent to the Twitter API
        payload = {}

        if 'username' not in extra_params.keys():
            err = "unfollow_user() action called without a 'username' key specified in the params dict."
            logger.error(err)
            raise Exception(err)
        else: 
            payload['user_id'] = extra_params['username']

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
        
        logger.info(content)





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

        logger = logging.getLogger('rainbowmindmachine')
        msg = self.timestamp_message("Finished populating a new tweet queue with %d tweets."%(len(tweet_queue)))
        logger.info(msg)

        return tweet_queue



    def tweet(self, extra_params, media=None):
        """
        tweet() handles scheduling.

        Run an infinity loop in which the bot decides when to tweet.

        Default Sheep have the following scheduling parameters:
        
            inner_sleep         Inner loop sleep time (1 s)
            outer_sleep         Outer loop sleep time (10 s)
            publish             Actually publish (False)

        Additional parameters:

            media               A URL, a local file, or a file-like object (something with a read() method)
                                or a list of any of the above

        This function never ends, so it never returns.
        """

        # --------------------------
        # Process parameters

        # Default parameter values
        defaults = {}
        defaults['inner_sleep'] = 1.0
        defaults['outer_sleep'] = 10.0
        defaults['publish'] = False
        #defaults['tweet_metadata'] = {}

        # populate missing params with default values
        for dk in defaults.keys():
            if dk not in extra_params.keys():
                extra_params[dk] = defaults[dk]

        # --------------------------
        # The Real McCoy
        #
        # call populate_queue() to populate the list of tweets to send out
        # 
        # apply some rube goldberg logic to figure out when to tweet each item

        logger = logging.getLogger('rainbowmindmachine')

        while True:

            try:
                
                # Outer loop
                tweet_queue = self.populate_queue()

                assert (len(tweet_queue)>0)

                for ii in range(len(tweet_queue)):

                    twit = tweet_queue.popleft()

                    # Fire off the tweet
                    if extra_params['publish']:

                        if(media is None):
                            self._tweet( twit )
                        else:
                            self._tweet( twit, media=media )

                    else:
                        self._print( twit )


                    time.sleep( extra_params['inner_sleep'] )

                time.sleep( extra_params['outer_sleep'] )

                msg = self.timestamp_message("Completed a cycle.")
                logger.info(msg)


            except Exception:

                # oops!

                msg1 = self.timestamp_message("Sheep encountered an exception. More info:")
                msg2 = self.timestamp_message(traceback.format_exc())
                msg3 = self.timestamp_message("Sheep is continuing...")

                logger.info(msg1)
                logger.info(msg2)
                logger.info(msg3)

                time.sleep( extra_params['outer_sleep'] )

            except AssertionError:

                err = "Error: tweet queue was empty. Check your populate_queue() method definition."
                logger.error(err)
                raise Exception(err)


    def _tweet(self,twit,media=None):
        """
        Private method.
        Publish a twit.
        """
        # call twitter api to tweet the twit

        logger = logging.getLogger('rainbowmindmachine')

        try:
            # tweet:
            if(media is not None):
                stats = self.api.PostUpdates(twit,media=media)
            else:
                stats = self.api.PostUpdates(twit)

            # everything else:
            msg = self.timestamp_message(">>> "+twit)
            logger.info(msg)

        except twitter.TwitterError as e:
            
            if e.message[0]['code'] == 185:
                msg = self.timestamp_message("Twitter error: Daily message limit reached")
                logger.info(msg)

            elif e.message[0]['code'] == 187:
                msg = self.timestamp_message("Twitter error: Duplicate error")
                logger.info(msg)
            
            else:
                msg = self.timestamp_message("Twitter error: "+e.message)
                logger.info(msg)


        ## DEBUG
        #self._print(twit)
        ## END DEBUG



    def _print(self,twit):
        """
        Private method.
        Print a twit.
        """
        logger = logging.getLogger('rainbowmindmachine')
        msg = self.timestamp_message("> "+twit)
        logger.info(msg)


    def timestamp_message(self,message):
        """
        Add a timestamp and a user handle to a message for logging purposes.
        """
        result = "[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " @" + self.params['screen_name']+"] " + message
        return result

