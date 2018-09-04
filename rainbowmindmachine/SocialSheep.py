from .TwitterSheep import TwitterSheep
import twitter
import traceback
import time


"""
Social Sheep

This is the base class for social sheep.
Social sheep basically add the ability to
interact with the twitterverse via a pool
of tweets (matching a hashtag, search term,
user, etc.)

NOTE: SocialSheep could even be used
as a "flock" for a single account.



The Social Sheep class also requires 
two other classes:

    Toilet - a small pool of tweets

We define all of these classes in one file,
mainly to challenge ourselves to keep it short.
"""


##########################
# SocialSheep class

class SocialSheep(TwitterSheep):
    """
    SocialSheep receive parameters from their keys.
    Let Sheep take care of the constructor.
    """


    #############################
    # Toilet class

    class Toilet(object):
        """
        The Toilet class creates a small pool of tweets.

        This class is only defined within the scope of SocialSheep.
        No other classes can use this Toilet.
        SocialSheep are *not* social about their Toilets.
        """

        #############################
        # BurdHurd class

        class BurdHurd(list):
            """
            The simplest class evar.

            Sometimes you can hear the Toilet 
            whispering to the BurdHurd: 
                
                "no one will ever know about you except me."
            """
            pass

        ####################################
        # Ok, on with the Toilet class

        def __init__(self, api, **kwargs):
            """
            The Toilet uses the SocialSheep's api and params.
            """
            self.api = api
            self.name = kawrgs['screen_name']
            if 'capacity' in kwargs:
                self.capacity = int(kwargs['capacity'])
            else:
                self.capacity = 100
    
        def flush(self, **kwargs):
            """
            Flush the toilet (get fresh tweets).
            
            Currently only one parameter:

                search_terms     String to search for

                ignore_threads  Whether to :ignore: tweets that occur somewhere
                                inside (potentially long) threads

            """
            if 'search_terms' in kwargs:
                search_terms = kwargs['search_terms']
            else:
                err = "SocialSheep Toilet Error: flush(): called SocialSheep flush() without search term.\n"
                err += "Specify search_terms kwarg: flush(search_terms = '...')"
                logging.error(self.sign_message(err), exc_info=True)
                raise Exception(err)

            if 'ignore_by' in kwargs:
                ignore_by = kwargs['ignore_by']
            else:
                ignore_by = []

            def stripat(s):
                if s[0]=='@':
                    return s[1:]
                else:
                    return s
            
            ignore_by = [stripat(j) for j in ignore_by]

            self.bowl = []
            for search_term in search_terms:

                results = self.api.GetSearch( term=search_term,
                                              count=self.capacity)

                for tweet in results:

                    # Always ignore retweets
                    not_retweet = tweet.text[0:2]!='RT' and tweet.in_reply_to_status_id is None

                    # Allow bot to ignore list of specific users
                    not_ignore_by = tweet.user.screen_name not in ignore_by

                    # Ensure the tweet actually has the search term, b/c 
                    # people at Twitter don't know what "search" means
                    has_search_term = search_term in tweet.text

                    if not_retweet:
                        if not_ignore_by:
                            if has_search_term:
                                self.bowl.append(tweet)

            # self.bowl is a list of Status objects
            # this is really useful:
            # http://python-twitter.readthedocs.io/en/latest/_modules/twitter/models.html#Status
            # 
            # so is this:
            # https://github.com/bear/python-twitter/blob/e17af0e67b7270ae448908ad44235d03562509eb/twitter/models.py
            # 
            # a BurdHurd is just a list of usernames
            # pulled straight out of the toilet.
            self.hurd = self.BurdHurd()
            for s in self.bowl:
                self.hurd.append(s.user)
    
        def favorite(self):
            """Favorite every tweet in the toilet."""
            for s in self.bowl:
                try:
                    self.api.CreateFavorite(status=s)
                    msg = "SocialSheep: favorite(): favorited tweet:\n"
                    msg += "    [@%s] : %s\n"%(s.user.screen_name, s.text)
                    eprint(msg)
                except twitter.error.TwitterError:
                    # already faved
                    pass
    
        def retweet(self):
            """Retweet every tweet in the toilet"""
            for s in self.bowl:
                try:
                    self.api.PostRetweet(status_id=s.id)
                    msg = "SocialSheep: retweet(): Retweeted tweet:\n"
                    msg += "    [@%s] : %s\n"%(s.user.screen_name, s.text)
                    eprint(msg)
                except:
                    # o noes!!! keep going
                    pass

        def follow(self):
            """
            Follow all users in a BurdHurd
            """
            # self.hurd is a list of strings (usernames)
            for u in self.hurd:
                try:
                    self.api.CreateFriendship(screen_name=u.screen_name)
                except twitter.error.TwitterError:
                    # following ourselves,
                    # or cannot find user
                    pass

        def sign_message(self,msg):
            """
            Given a message, prepend it with [@botname]
            (this is for Toilet, not Sheep)
            """
            result = "[@%s] %s"%(self.name, msg)
            return result



    #############################################
    # Ok, on with the SocialSheep class

    def __init__(self, json_file, **kwargs):
        """
        SocialSheep constructor calls the Sheep constructor,
        which sets the Sheep's parameter values.

        It then calls a Plumber to install a Toilet.

        kwargs:
            capacity        Number of tweets in the toilet
        """
        # Call super constructor
        super().__init__(json_file, **kwargs)

        # Now call a plumber to have a toilet installed
        self._call_plumber(**kwargs)


    def _call_plumber(self,**kwargs):
        """
        Call a plumber to install a Toilet
        """
        # Toilets take parameters for their search.
        # These come from the SocialSheep's parameters.
        self.toilet = self.Toilet(self.api,**kwargs)


    def favorite(self, **kwargs):
        """
        Favorite all the tweets in the toilet

        kwargs:
            sleep: Time to sleep between flushes
            follow: boolean, should we follow all the tweeters in the toilet

        The call to flush passes along all of the parameters. 
        The flush function takes the following parameter:

        kwargs:
            search_terms: Strings to search for

        This function never ends, so it never returns.
        """
        if('follow' not in kwargs.keys()):
            kwargs['follow'] = False

        if('sleep' not in kwargs.keys()):
            err = "SocialSheep Error: favorite(): Called SocialSheep favorite() without search term.\n"
            err += "Specify search_terms kwarg: flush(search_terms = ['a','b',...])"
            logging.error(self.sign_message(err), exc_info=True)
            raise Exception(err)

        while True:

            try:
                self.toilet.flush(**kwargs)
            except Exception:
                err = "SocialSheep Error: favorite(): Encountered exception flush()ing tweets in the Toilet"
                logging.error(self.sign_message(err), exc_info=True)

            try:
                self.toilet.favorite()
            except Exception:
                err = "SocialSheep Error: favorite(): Encountered exception favorite()ing tweets in the Toilet"
                logging.error(self.sign_message(err), exc_info=True)

            if kwargs['follow']:
                try:
                    self.toilet.follow()
                except Exception:
                    err = "SocialSheep Error: favorite(): Encountered exception follow()ing tweets in the Toilet"
                    logging.error(self.sign_message(err), exc_info=True)

            time.sleep( kwargs['sleep'] )


    def retweet(self, **kwargs):
        """
        Retweet all the tweets in the toilet

        kwargs:
            sleep: Time to sleep between flushes
            follow: boolean, should we follow all the tweeters in the toilet

        The call to flush passes along all of the parameters. 
        The flush function takes the following parameter:

        kwargs:
            search_terms: Strings to search for

        This function never ends, so it never returns.
        """
        if('follow' not in kwargs.keys()):
            kwargs['follow'] = False

        if('sleep' not in kwargs.keys()):
            err = "SocialSheep Error: retweet(): called SocialSheep retweet() without search term.\n"
            err += "Specify search_terms kwarg: flush(search_terms = ['a','b',...])"
            logging.error(self.sign_message(err), exc_info=True)
            raise Exception(err)

        while True:

            try:
                self.toilet.flush(**kwargs)
            except Exception:
                err = "ERROR: SocialSheep encountered exception flush()ing tweets in the Toilet"
                logging.error(self.sign_message(err), exc_info=True)

            try:
                self.toilet.retweet()
            except Exception:
                err = "ERROR: SocialSheep encountered exception retweet()ing tweets in the Toilet"
                logging.error(self.sign_message(err), exc_info=True)

            if kwargs['follow']:
                try:
                    self.toilet.follow()
                except Exception:
                    err = "ERROR: SocialSheep encountered exception follow()ing tweets in the Toilet"
                    logging.error(self.sign_message(err), exc_info=True)

            time.sleep( kwargs['sleep'] )


    def follow(self, **kwargs):
        """
        Follow all the tweeters in the toilet

        kwargs:
            sleep: Time to sleep between flushes

        Call to flush passes along all of the parameters. 
        The flush function takes the following parameter:

        kwargs:
            search_terms: Strings to search for

        This function never ends, so it never returns.
        """
        if('sleep' not in kwargs.keys()):
            err = "ERROR: called SocialSheep favorite() without search term.\n"
            err += "Specify search_terms kwarg: flush(search_terms = '...')"
            raise Exception(err)

        while True:

            try:
                self.toilet.flush(**kwargs)
            except Exception:
                err = "SocialSheep Error: follow(): Encountered exception flush()ing toilet"
                logging.error(self.sign_message(err), exc_info=True)

            try:
                self.toilet.favorite()
            except Exception:
                err = "SocialSheep Error: follow(): Encountered exception favorite()ing toilet"
                logging.error(self.sign_message(err), exc_info=True)

            time.sleep( kwargs['sleep'] )

