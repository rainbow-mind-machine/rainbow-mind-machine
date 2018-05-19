import twitter
from .Sheep import Sheep

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




class SocialSheep(Sheep):
    """
    SocialSheep receive parameters from their keys.
    Let Sheep take care of the constructor.
    """

    #############################
    # BurdHurd class

    class BurdHurd(list):
        """
        The simplest class evar
        """
        pass


    #############################
    # Toilet class

    class Toilet(object):
        """
        The Toilet class creates a small pool of tweets.

        This class is only defined within the scope of SocialSheep.
        No other classes can use this Toilet.
        SocialSheep are *not* social about their Toilets.
        """
        def __init__(self, api, params):
            """
            The Toilet uses the SocialSheep's api and params.
            """
            self.api = api
            self.params = params

            # Don't assume params contains search parameters.
            # Do some validation here.
    
        def flush(self):
            """Flush the toilet (get fresh tweets)"""
            self.bowl = list(api.GetSearch(terms='#rainbowmindmachine',count=10))

            # self.bowl is a list of Status objects
            # this is really useful:
            # http://python-twitter.readthedocs.io/en/latest/_modules/twitter/models.html#Status
            # 
            # a BurdHurd is just a list of usernames
            # pulled straight out of the toilet.
            self.hurd = BurdHurd()
            for s in self.bowl:
                self.hurd.append(s['user'])
    
        def favorite(self):
            """Favorite every tweet in the toilet"""
            for s in self.bowl:
                api.CreateFavorite(status=s)
    
        def retweet(self):
            """Retweet every tweet in the toilet"""
            for s in self.bowl:
                api.PostRetweet(status_id=s['id'])

        def follow(self):
            """
            Follow all users in a BurdHurd
            """
            # self.hurd is a list of strings (usernames)
            for u in self.hurd:
                api.CreateFriendship(screen_name=u)



    #############################
    # SocialSheep class

    def __init__(self, json_file, **kwargs):
        """
        SocialSheep constructor calls the Sheep constructor,
        which sets the Sheep's parameter values.

        It then calls a Plumber to install a Toilet.
        """
        # Call super constructor
        super().__init__(self, json_file, **kwargs)

        # Now call a plumber to have a toilet installed
        self._call_plumber(self.api)
    

    def _call_plumber(self):
        """
        Call a plumber to install a Toilet
        """
        # Toilets take parameters for their search.
        # These come from the SocialSheep's parameters.
        self.toilet = Toilet(self.api, self.params)
        self.flush_the_toilet()


    def flush_the_toilet(self):
        """
        Flush the toilet to get some fresh tweets
        """
        self.toilet.flush()

    def favorite_toilet(self):
        """
        Favorite all the tweets in the toilet
        """
        self.toilet.favorite()

    def retweet_toilet(self):
        """
        Retweet all the tweets in the toilet
        """
        self.toilet.retweet()

    def follow_toilet(self):
        """
        Follow all the users in the toilet
        """
        self.toilet.follow()

    #def list_toilet(self, public=False):
    #    """Make a list from all the users in the toilet
    #    """
    #    self.toilet.make_list(public=public)


