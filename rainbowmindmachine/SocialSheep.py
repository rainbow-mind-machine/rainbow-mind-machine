from .Sheep import Sheep
import twitter
import logging
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

class SocialSheep(Sheep):
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

        def __init__(self, api):
            """
            The Toilet uses the SocialSheep's api and params.
            """
            self.api = api
    
        def flush(self, **kwargs):
            """
            Flush the toilet (get fresh tweets).
            
            Currently only one parameter:

                search_term     String to search for
            """
            if 'search_term' in kwargs:
                search_term = kwargs['search_term']
            else:
                err = "ERROR: called SocialSheep flush() without search term.\n"
                err += "Specify a search_term kwarg: flush(search_term = '...')"
                raise Exception(err)

            self.bowl = list(self.api.GetSearch(term=search_term,count=10))

            # self.bowl is a list of Status objects
            # this is really useful:
            # http://python-twitter.readthedocs.io/en/latest/_modules/twitter/models.html#Status
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
                except twitter.error.TwitterError:
                    # already faved
                    pass
    
        def retweet(self):
            """Retweet every tweet in the toilet"""
            for s in self.bowl:
                self.api.PostRetweet(status_id=s.id)

        def follow(self):
            """
            Follow all users in a BurdHurd
            """
            # self.hurd is a list of strings (usernames)
            for u in self.hurd:
                try:
                    self.api.CreateFriendship(screen_name=u.screen_name)
                    logger = logging.getLogger('rainbowmindmachine')
                    logger.info("Started following @%s"%(u.screen_name))
                except twitter.error.TwitterError:
                    # following ourselves,
                    # or cannot find user
                    pass



    #############################################
    # Ok, on with the SocialSheep class

    def __init__(self, json_file, **kwargs):
        """
        SocialSheep constructor calls the Sheep constructor,
        which sets the Sheep's parameter values.

        It then calls a Plumber to install a Toilet.
        """
        # Call super constructor
        super().__init__(json_file, **kwargs)

        # Now call a plumber to have a toilet installed
        self._call_plumber()


    def _call_plumber(self):
        """
        Call a plumber to install a Toilet
        """
        # Toilets take parameters for their search.
        # These come from the SocialSheep's parameters.
        self.toilet = self.Toilet(self.api)


    def favorite(self, **kwargs):
        """
        Favorite all the tweets in the toilet

        Parameters:

            sleep           Time to sleep between flushes

        Call to flush passes along all of the parameters. 
        The flush function takes the following parameter:
            
            search_term     String to search for

        This function never ends, so it never returns.
        """
        defaults = {}
        defaults['sleep'] = 1.0

        # populate missing params with default values
        extra_params = kwargs
        for dk in defaults.keys():
            if dk not in extra_params.keys():
                extra_params[dk] = defaults[dk]

        logger = logging.getLogger('rainbowmindmachine')

        while True:

            try:
                self.toilet.flush(**kwargs)
            except Exception:
                err = "ERROR: SocialSheep encountered exception flush()ing toilet"
                logger.info(self.timestamp_message(err))
                logger.info(self.timestamp_message(traceback.format_exc()))


            try:
                self.toilet.favorite()
            except Exception:
                err = "ERROR: SocialSheep encountered exception favorite()ing toilet"
                logger.info(self.timestamp_message(err))
                logger.info(self.timestamp_message(traceback.format_exc()))



            try:
                self.toilet.follow()
            except Exception:
                err = "ERROR: SocialSheep encountered exception follow()ing toilet"
                logger.info(self.timestamp_message(err))
                logger.info(self.timestamp_message(traceback.format_exc()))


            time.sleep( extra_params['sleep'] )


    def retweet(self):
        """
        Retweet all the tweets in the toilet
        """
        self.toilet.retweet()

    def follow(self):
        """
        Follow all the users in the toilet
        """
        self.toilet.follow()

