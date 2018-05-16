import twitter

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

class Toilet(object):
    """
    The Toilet class creates a small pool of tweets.
    """
    def __init__(self, api, params):
        self.api = api
        self.params = params


class SocialSheep(Sheep):
    """
    SocialSheep receive parameters from their keys.
    Let Sheep take care of the constructor.
    """
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
        """Call a plumber to install a Toilet
        """
        # Toilets take parameters for their search.
        # These come from the SocialSheep's parameters.
        self.toilet = Toilet(self.api, self.params)
        self.flush_the_toilet()


    def flush_the_toilet(self):
        """Flush the toilet to get some fresh tweets
        """
        self.toilet.flush()

    def favorite_toilet(self):
        """Favorite all the tweets in the toilet
        """
        pass

    def retweet_toilet(self):
        """Retweet all the tweets in the toilet
        """
        pass

    def follow_toilet(self):
        """Follow all the users in the toilet
        """
        user_list = pull_users_from_toilet()

    def list_toilet(self, public=False):
        """Make a list from all the users in the toilet
        """
        pass

    def pull_users_from_toilet(self):
        """Pull out a list of users from the toilet
        """
        users = self.toilet.get_users()





