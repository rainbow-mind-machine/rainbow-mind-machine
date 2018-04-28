import urllib
import oauth2 as oauth
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
    - json file is stored as self.params and contains everything the sheep needs
    - by default, bot tweeting is two-layered:
        - outer loop populates tweet queue
        - inner loop tweets from the tweet queue
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

        self.lumberjack = lumberjack

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
        self.lumberjack.log(msg)


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
        if( 'url' not in extra_params.keys()):
            # what are you doing??
            raise Exception("change_url() action called without 'url' key specified in the parameters dict.")

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
        
        self.lumberjack.log(content)



    def change_bio(self,extra_params):
        """
        Update twitter profile bio

        Parameters:
        bio         The bio string

        Does not return anything
        """
        if( 'bio' not in extra_params.keys()):
            # what are you doing??
            err = "change_bio() action called without 'bio' key specified in the parameters dict."
            self.lumberjack.log(err)
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
        
        self.lumberjack.log(content)


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
        if( 'background' not in extra_params.keys() and 'links' not in extra_params.keys()):
            # what are you doing??
            err = "change_color() action called without 'background' or 'links' keys specified in the parameters dict."
            self.lumberjack.log(err)
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
        
        self.lumberjack.log(content)



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
        # json sent to the Twitter API
        payload = {}

        if 'image' not in extra_params.keys():
            # what are you doing?
            err = "change_image() action called without an 'image' key specified in the params dict."
            self.lumberjack.log(err)
            raise Exception(err)
        elif os.path.isfile(extra_params['image']) is False:
            err = "change_image() action called with 'image' key of params dict pointing to a non-existent file."
            self.lumberjack.log(err)
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
        
        self.lumberjack.log(content)



    def follow_user(self, extra_params, notify=True):
        """
        Follow a twitter user

        Parameters:
        username        The username of the user to follow
        notify          Whether to notify the followed user (boolean)

        This method does not return anything
        """
        # json sent to the Twitter API
        payload = {}

        if 'username' not in extra_params.keys():
            # what are you doing?
            err = "follow_user() action called without a 'username' key specified in the params dict."
            self.lumberjack.log(err)
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
        
        self.lumberjack.log(content)


    def unfollow_user(self, extra_params, notify=True):
        """
        Unfollow a twitter user

        Parameters:
        username        The username of the user to unfollow

        This method does not return anything
        """
        # json sent to the Twitter API
        payload = {}

        if 'username' not in extra_params.keys():
            # what are you doing?
            err = "unfollow_user() action called without a 'username' key specified in the params dict."
            self.lumberjack.log(err)
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
                self.lumberjack.log(msg)


            except Exception:

                # oops!

                msg1 = self.timestamp_message("Sheep encountered an exception. More info:")
                msg2 = self.timestamp_message(traceback.format_exc())
                msg3 = self.timestamp_message("Sheep is continuing...")

                self.lumberjack.log(msg1)
                self.lumberjack.log(msg2)
                self.lumberjack.log(msg3)

                time.sleep( extra_params['outer_sleep'] )

            except AssertionError:
                raise Exception("Error: tweet queue was empty. Check your populate_queue() method definition.")


    def _tweet(self,twit,media):
        """
        Private method.
        Publish a twit.
        """
        # call twitter api to tweet the twit

        try:
            # tweet:
            if(media is not None):
                stats = self.api.PostUpdates(twit,media=media)
            else:
                stats = self.api.PostUpdates(twit)

            # everything else:
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

