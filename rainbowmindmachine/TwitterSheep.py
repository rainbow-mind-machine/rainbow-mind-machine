import boringmindmachine as bmm
import os, time, datetime, urllib
import twitter
import traceback
import base64
import oauth2 as oauth
import simplejson as json

from .utils import eprint

class TwitterSheep(bmm.BoringSheep):
    """
    Twitter Sheep class.

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

        msg = "rainbow-mind-machine: TwitterSheep: Set up Twitter API for bot {screen_name}"
        msg = msg.format(screen_name=self.params['screen_name'])
        eprint(msg)


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
        if( 'url' not in kwargs.keys()):
            err = "ERROR: rmm Sheep: change_url() action called without 'url' kwarg specified."
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

        eprint("Completed change_url() method. Set url to: %s"%(bot_url))


    def change_bio(self,**kwargs):
        """Update twitter profile bio.

        kwargs:
            bio: The bio string

        Does not return anything.
        """
        if( 'bio' not in kwargs.keys()):
            err = "change_bio() action called without 'bio' key specified in the parameters dict."
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

        eprint("Completed change_bio() method.")
        eprint(content)


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
        if( 'background' not in kwargs.keys()
                and 'links' not in kwargs.keys()):
            err = "ERROR: rmm Sheep: change_colors() action called "
            err += "with neither 'background' nor 'links' kwargs specified."
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

        eprint("Completed change_colors() method.")
        eprint(content)


    def change_image(self,**kwargs):
        """Update twitter profile bio.

        Setting 'image' keyword argument takes the highest
        priority and is the image used if present.

        If that is not available, change_image() will look
        for an 'image' keyword argument in the bot key.

        kwargs:
            image: The path to the image to use as the Twitter avatar

        This method does not return anything.
        """
        if( 'image' not in kwargs.keys() and 'image' not in self.params):
            err = "change_image() action called without 'image' key specified in the bot key or the parameters dict."
            raise Exception(err)

        img_file = ''
        if( 'image' in kwargs.keys() ):
            img_file = kwargs['image']
            if os.path.isfile(img_file) is False:
                err = "change_image() action called with an 'image' key that is not a file!"
                raise Exception(err)
        elif( 'image' in self.params ):
            img_file = self.params['image']
            if os.path.isfile(img_file) is False:
                err = "change_image() action called with an 'image' key that is not a file!"
                raise Exception(err)

        # json sent to the Twitter API
        payload = {}

        b64 = base64.encodestring(open(img_file,"rb").read())

        # Set the API endpoint 
        api_url = "https://api.twitter.com/1.1/account/update_profile_image.json"

        resp, content = self.client.request(
                api_url,
                method = "POST",
                body=urllib.parse.urlencode({'image': b64}),
                headers=None
        )

        eprint("Completed change_image() method.")
        eprint(content)


    def follow_user(self, **kwargs):
        """
        Follow a twitter user.

        kwargs:
            username: The username of the user to follow
            notify: Whether to notify the followed user (boolean)

        This method does not return anything.
        """
        if( 'username' not in kwargs.keys()):
            err = "change_image() action called without 'image' key specified in the parameters dict."
            raise Exception(err)

        if( 'notify' not in kwargs.keys()):
            kwargs['notify'] = False

        # json sent to the Twitter API
        payload = {}

        # Set the API endpoint 
        url = "https://api.twitter.com/1.1/friendships/create.json"

        resp, content = self.client.request(
                api_url,
                method = "POST",
                body=urllib.urlencode({'image': b64}),
                headers=None
        )

        eprint("Completed follow_user() method.")
        eprint(content)


    def unfollow_user(self, notify=True, **kwargs):
        """
        Unfollow a twitter user.

        kwargs:
            username: The username of the user to follow
            notify: Whether to notify the followed user (boolean)

        This method does not return anything.
        """
        if 'username' not in kwargs.keys():
            err = "unfollow_user() action called without a 'username' key specified in the params dict."
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

        eprint("Completed unfollow_user() method.")
        eprint(content)


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

                msg = "rainbow-mind-machine: TwitterSheep: Completed a cycle."
                eprint(msg)

            except Exception:

                # oops!

                msg1 = "rainbow-mind-machine: Sheep encountered an exception. More info:"
                msg2 = traceback.format_exc()
                msg3 = "rainbow-mind-machine: Sheep is continuing..."

                eprint(msg1)
                eprint(msg2)
                eprint(msg3)

                time.sleep( kwargs['outer_sleep'] )

            except AssertionError:

                err = "Error: tweet queue was empty. Check your populate_tweet_queue() method definition."
                raise Exception(err)


    def _tweet(self,twit,media=None):
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
            msg = "rainbow-mind-machine: TwitterSheep: @%s tweeted: \"%s\""%(self.name, twit)
            eprint(msg)

        except twitter.TwitterError as e:
            
            if e.message[0]['code'] == 185:
                msg = "rainbow-mind-machine: TwitterSheep: Twitter error: Daily message limit reached"
                eprint(msg)

            elif e.message[0]['code'] == 187:
                msg = "rainbow-mind-machine: TwitterSheep: Twitter error: Duplicate error"
                eprint(msg)
            
            else:
                msg = "rainbow-mind-machine: TwitterSheep: Twitter error: %s"%(e.message)
                eprint(msg)


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

        msg = "rainbow-mind-machine: TwitterSheep: Finished populating a new tweet queue with %d tweets."%(len(tweet_queue))
        eprint(msg)

        return tweet_queue


    def _print(self,twit):
        """
        Private method.
        Print a twit.
        """
        msg = "rainbow-mind-machine: TwitterSheep: @%s printed: \"%s\""%(self.name, twit)
        eprint(msg)

