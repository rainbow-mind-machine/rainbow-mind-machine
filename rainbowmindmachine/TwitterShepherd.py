import boringmindmachine as bmm

"""
rmm.Shepherd

We only need to define two methods:

        _validate_key(self,bot_key)

        _create_sheep(self,bot_key)
"""

class TwitterShepherd(bmm.BoringShepherd):

    def _validate_key(self, bot_key, **kwargs):
        """
        Validate the Twitter keys made by the Keymaker
        """
        required_keys = ['consumer_token',
                         'consumer_token_secret',
                         'oauth_token',
                         'oauth_token_secret',
                         'screen_name']
        for key in required_keys:
            if key not in bot_key.keys():
                err = "ERROR: rmm.Shepherd encountered an invalid bot key.\n"
                err += "The bot key is missing a value for '%s'."%(key)
                raise Exception(err)

    def _create_sheep(self, bot_key, **kwargs):
        """
        If the key is valid, create a Sheep with it
        """
        sheep = self.sheep_class(bot_key)
        self.flock.append(sheep)

