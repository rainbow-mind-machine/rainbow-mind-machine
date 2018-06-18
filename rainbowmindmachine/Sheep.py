import boringmindmachine as bmm
import logging
import urllib
import oauth2 as oauth
import twitter
import time
import simplejson as json
import datetime
import traceback
import base64


class Sheep(bmm.BoringSheep):
    """
    rainbow mind machine Sheep class.

    Sheep are created by the Shepherd.
    Sheep are initialized with a JSON key file plus parameters from the Shepherd.
    Sheep are expected to take care of their own API instance.

    Input bot key (JSON file) is stored as self.params and contains everything the sheep needs
    """
    def __init__(self, bot_key, **kwargs):
        """
        bot_key - parameters that come from the keys (and the Keymaker, and the key-making process)
            - consumer_token
            - consumer_token_secret
            - oauth_token
            - oauth_token_secret
            - user_id
            - screen_name
        
        kwargs - extra parameter args passed 
                 into the Sheep (from the Shepherd)
        
        A Sheep object manages information for a single Twitter bot account.
        The information (oauth keys, bot name, bot account, etc) are contained
        in the JSON file passed in by the Shepherd.
        
        The JSON file contains information compiled by the Keymaker.
        If there is other information the Shepherd needs to pass to the 
        Sheep that is not in the JSON file, it can use keyword args.
        """

        # This is where we should initialize the Twitter API instance 
        # using params found in the json file.

        self.params = bot_key
 
        # combine the user-provided parameters 
        # (in kwargs) with the json-provided parameters
        for keys in kwargs:
            self.params[key] = kwargs[key]

        # Initialize your API instance
        self.api = twitter.Api( consumer_key        = self.params['consumer_token'],
                                consumer_secret     = self.params['consumer_token_secret'],
                                access_token_key    = self.params['oauth_token'],
                                access_token_secret = self.params['oauth_token_secret'])

        # Get an OAuth token to do bot stuff
        self.token = oauth.Token(
                key = self.params['oauth_token'], 
                secret = self.params['oauth_token_secret']
        )

        # Add an OAuth application to consume the API
        self.consumer = oauth.Consumer(
                key = self.params['consumer_token'], 
                secret = self.params['consumer_token_secret']
        )

        # Create an OAuth client
        self.client = oauth.Client(
                self.consumer,
                self.token
        )

        # Set names
        self.name = bot_key['screen_name']
        self.flock_name = bot_key['flock_name']

        logger = logging.getLogger('rainbowmindmachine')
        msg = "Set up Twitter API for bot {screen_name}"
        msg = msg.format(screen_name=self.params['screen_name'])
        logger.info(msg)


    #####################################
    # rainbow mind machine Sheep:
    # non-Twitter actions

    def dummy(self, **kwargs):
        """Debug: do nothing."""
        pass

    def echo(self, **kwargs):
        """Just say hi"""
        print("Hello world! This is {name}".format(name=self.name))


    #################################
    # rainbow mind machine Sheep:
    # Twitter actions
    # 
    # change_url
    # change_bio
    # change_color
    # change_image
    # tweet
    # follow_user
    # unfollow_user

    def change_url(self, **kwargs):
        """Update twiter profile URL.

        kwargs:
            url:    The new url (string) to set as the profile URL

        Does not return anything.
        """
        logger = logging.getLogger('rainbowmindmachine')

        if( 'url' not in kwargs.keys()):
            err = "ERROR: rmm Sheep: change_url() action called without 'url' kwarg specified."
            logger.error(err)
            raise Exception(err)

        # Set the API endpoint 
        api_url = "https://api.twitter.com/1.1/account/update_profile.json"

        bot_url = kwargs['url']

        resp, content = self.client.request(
                api_url,
                method = "POST",
                body = urllib.parse.urlencode({'url':bot_url}),
                headers = None
        )

        logger.info("Completed change_url() method. Set url to: %s"%(bot_url))


    def change_bio(self,**kwargs):
        """Update twitter profile bio.

        kwargs:
            bio: The bio string

        Does not return anything.
        """
        logger = logging.getLogger('rainbowmindmachine')

        if( 'bio' not in kwargs.keys()):
            err = "change_bio() action called without 'bio' key specified in the parameters dict."
            logger.error(err)
            raise Exception(err)

        # Set the API endpoint 
        url = "https://api.twitter.com/1.1/account/update_profile.json"

        bot_bio = kwargs['bio']
        resp, content = self.client.request(
                url,
                method = "POST",
                body=urllib.urlencode({'description': bot_bio}),
                headers=None
        )

        logger.info("Completed change_bio() method.")
        logger.info(content)


    def change_colors(self,**kwargs):
        """
        Update twitter profile colors.

        kwargs:
            background: RGB code for background color (no #)
            links: RGB code for links color (no #)
        
        Example:
            kwargs = {
                'background':'3D3D3D', 
                'link':'AAF'
            }

        Does not return anything.
        """
        logger = logging.getLogger('rainbowmindmachine')

        if( 'background' not in kwargs.keys()
                and 'links' not in kwargs.keys()):
            err = "ERROR: rmm Sheep: change_colors() action called "
            err += "with neither 'background' nor 'links' kwargs specified."
            logger.error(err)
            raise Exception(err)

        # json sent to the Twitter API
        payload = {}

        if 'background' in kwargs.keys():
            background_rgbcode = kwargs['background']
            payload['profile_background_color'] = background_rgbcode

        if 'links' in kwargs.keys():
            links_rgbcode = kwargs['links']
            payload['profile_link_color'] = links_rgbcode

        # Set the API endpoint 
        url = "https://api.twitter.com/1.1/account/update_profile_colors.json"

        resp, content = self.client.request(
                url,
                method = "POST",
                body=urllib.urlencode(payload),
                headers=None
        )

        logger.info("Completed change_colors() method.")
        logger.info(content)


    def change_image(self,**kwargs):
        """Update twitter profile bio.

        kwargs:
            image: The path to the image to use as the Twitter avatar

        Note that unlike most actions, the parameter
        passed in by the user must be pre-processed first.

        This method does not return anything.
        """
        logger = logging.getLogger('rainbowmindmachine')

        if( 'image' not in kwargs.keys()):
            err = "change_image() action called without 'image' key specified in the parameters dict."
            logger.error(err)
            raise Exception(err)

        if os.path.isfile(kwargs['image']) is False:
            err = "change_image() action called with 'image' key of params dict pointing to a non-existent file."
            logger.error(err)
            raise Exception(err)

        # json sent to the Twitter API
        payload = {}

        img_file = kwargs['image']
        b64 = base64.encodestring(open(img_file,"rb").read())

        # Set the API endpoint 
        api_url = "https://api.twitter.com/1.1/account/update_profile_image.json"

        resp, content = client.request(
                api_url,
                method = "POST",
                body=urllib.urlencode({'image': b64}),
                headers=None
        )

        logger.info("Completed change_image() method.")
        logger.info(content)


    def follow_user(self, **kwargs):
        """
        Follow a twitter user.

        kwargs:
            username: The username of the user to follow
            notify: Whether to notify the followed user (boolean)

        This method does not return anything.
        """
        logger = logging.getLogger('rainbowmindmachine')

        if( 'username' not in kwargs.keys()):
            err = "change_image() action called without 'image' key specified in the parameters dict."
            logger.error(err)
            raise Exception(err)

        if( 'notify' not in kwargs.keys()):
            kwargs['notify'] = False

        # json sent to the Twitter API
        payload = {}

        # Set the API endpoint 
        url = "https://api.twitter.com/1.1/friendships/create.json"

        resp, content = client.request(
                api_url,
                method = "POST",
                body=urllib.urlencode({'image': b64}),
                headers=None
        )

        logger.info("Completed follow_user() method.")
        logger.info(content)


    def unfollow_user(self, notify=True, **kwargs):
        """
        Unfollow a twitter user.

        kwargs:
            username: The username of the user to follow
            notify: Whether to notify the followed user (boolean)

        This method does not return anything.
        """
        logger = logging.getLogger('rainbowmindmachine')

        if 'username' not in kwargs.keys():
            err = "unfollow_user() action called without a 'username' key specified in the params dict."
            logger.error(err)
            raise Exception(err)

        if( 'notify' not in kwargs.keys()):
            kwargs['notify'] = False

        # json sent to the Twitter API
        payload = {}

        # Set the API endpoint 
        url = "https://api.twitter.com/1.1/friendships/destroy.json"

        payload['user_id'] = kwargs['username']

        resp, content = self.client.request(
                url,
                method = "POST",
                body=urllib.urlencode(payload),
                headers=None
        )

        logger.info("Completed unfollow_user() method.")
        logger.info(content)


    def tweet(self, **kwargs):
        """
        Send out a tweet. This uses the function:

            populate_tweet_queue()

        Run an infinity loop in which the bot decides when to tweet.

        Default Sheep have the following scheduling kwargs:
        
        kwargs:
            inner_sleep: Inner loop sleep time (1 s)
            outer_sleep: Outer loop sleep time (10 s)
            publish: Actually publish (False)

        Additional kwargs:

            media: A URL, a local file, or a file-like object (something with a read() method)
                   or a list of any of the above

        This function never ends, so it never returns.
        """

        # Process kwargs
        defaults = {}
        defaults['inner_sleep'] = 1.0
        defaults['outer_sleep'] = 10.0
        defaults['publish'] = False

        # populate missing params with default values
        for dk in defaults.keys():
            if dk not in kwargs.keys():
                kwargs[dk] = defaults[dk]

        # --------------------------
        # The Real McCoy
        #
        # call populate_tweet_queue() to populate the list of tweets to send out
        # 
        # apply some rube goldberg logic to figure out when to tweet each item

        logger = logging.getLogger('rainbowmindmachine')

        while True:

            try:
                
                # Outer loop
                tweet_queue = self.populate_tweet_queue()
                nelements = len(tweet_queue)

                assert nelements>0

                for ii in range(nelements):

                    twit = tweet_queue.pop(0)

                    # Fire off the tweet
                    if kwargs['publish']:

                        if(media is None):
                            self._tweet( twit )
                        else:
                            self._tweet( 
                                    twit, 
                                    media = media 
                            )

                    else:
                        self._print( twit )


                    time.sleep( kwargs['inner_sleep'] )

                time.sleep( kwargs['outer_sleep'] )

                msg = "Completed a cycle."
                logger.info(msg)

            except Exception:

                # oops!

                msg1 = "Sheep encountered an exception. More info:"
                msg2 = traceback.format_exc()
                msg3 = "Sheep is continuing..."

                logger.info(msg1)
                logger.info(msg2)
                logger.info(msg3)

                time.sleep( kwargs['outer_sleep'] )

            except AssertionError:

                err = "Error: tweet queue was empty. Check your populate_tweet_queue() method definition."
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
            msg = "@%s tweeted: \"%s\""%(self.name, twit)
            logger.info(msg)

        except twitter.TwitterError as e:
            
            if e.message[0]['code'] == 185:
                msg = "Twitter error: Daily message limit reached"
                logger.info(msg)

            elif e.message[0]['code'] == 187:
                msg = "Twitter error: Duplicate error"
                logger.info(msg)
            
            else:
                msg = "Twitter error: %s"%(e.message)
                logger.info(msg)


    def populate_tweet_queue(self):
        """
        Populate a tweet queue.

        This method should be extended by new Sheep classes that have their own
        creative means of generating tweets.

        The default Sheep object will generate a tweet queue filled with
        5 "Hello World" messages.

        Returns a list of tweets.
        """
        maxlen = 5
        tweet_queue = []

        # (technically, a list is a queue)
        
        for j in range(maxlen):
            tweet = "Hello world! That's number %d of 5."%(j+1)
            tweet_queue.append(tweet)

        logger = logging.getLogger('rainbowmindmachine')
        msg = "Finished populating a new tweet queue with %d tweets."%(len(tweet_queue))
        logger.info(msg)

        return tweet_queue


    def _print(self,twit):
        """
        Private method.
        Print a twit.
        """
        logger = logging.getLogger('rainbowmindmachine')
        msg = "@%s printed: \"%s\""%(self.name, twit)
        logger.info(msg)

