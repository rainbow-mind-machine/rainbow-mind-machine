import boringmindmachine as bmm

"""
rmm.Shepherd

We only need to define two methods:

        _validate_key(self,bot_key)

        _create_sheep(self,bot_key)
"""

class TwitterShepherd(bmm.BoringShepherd):

    def __init__(self,
            json_keys_dir,
            sheep_class = bmm.TwitterSheep,
            **kwargs):
        """
        This constructor calls the Boring Shepherd constructor.

            json_keys_dir:  Directory where Sheep API keys are located

            sheep_class:    Type of Sheep

            kwargs:         Parameters passed on to the Sheep
        """
        super().__init__(
                json_keys_dir, 
                sheep_class=sheep_class, 
                **kwargs
        )

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
                err = "ERROR: TwitterShepherd encountered an invalid bot key.\n"
                err += "The bot key is missing a value for '%s'."%(key)
                raise Exception(err)

    def _create_sheep(self, bot_key, **kwargs):
        """
        If the key is valid, create a Sheep with it
        """
        sheep = self.sheep_class(bot_key)
        self.flock.append(sheep)

