import twitter
import os, re, time, glob
import simplejson as json

from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool 

from .Sheep import *
from .Lumberjack import *

its_alive = r'''
 _______ _______ __ _______      _______ _____   _______ ___ ___ _______ __ __ __
|_     _|_     _|  |     __|    |   _   |     |_|_     _|   |   |    ___|  |  |  |
 _|   |_  |   |  |_|__     |    |       |       |_|   |_|   |   |    ___|__|__|__|
|_______| |___|    |_______|    |___|___|_______|_______|\_____/|_______|__|__|__|
'''

class Shepherd(object):
    """
    Spin up the flock of Sheep and let them roam free
    """
    def __init__(self, 
                 json_keys_dir, 
                 flock_name,
                 sheep_class=Sheep, 
                 **kwargs):
        """
        Create a Shepherd.

            json_keys_dir:      Directory where Sheep API keys are located

            flock_name:         The name of the bot flock (used to format log messages)

            sheep_class:        Type of Sheep

            kwargs:             Logging parameters passed directly to Lumberjack logger

        For example, a flock of Queneau Sheep is created like this:

            sh = rmm.Shepherd(json_keys_dir = 'keys/',
                              flock_name = 'Queneau Flock',
                              sheep_class = rmm.QueneauSheep)

        To pass a custom log file name to lumberjack:

            sh = rmm.Shepherd(json_eys_dir = 'keys/',
                              flock_name = 'Plain Old Flock of Sheep',
                              log_file = '/path/to/my/log')
        """

        # save flock name
        self.name = flock_name

        # contains each of our sheep
        self.all_sheep = []

        # contains json files with Twitter acct keys
        # (one for each sheep)
        self.all_json = []

        # Create a Lumberjack instance to configure the logs.
        # This sets the log configuration for a logger named
        # 'rainbowmindmachine'
        # 
        # Rather saving lumberjack, we just say
        # logger = logging.getLogger('rainbowmindmachine')
        # logger.info('sjasdljflasdkjflksj')
        # 
        lumberjack = Lumberjack(**kwargs)
        # 
        # Set it and forget it, 
        # we don't need lumberjack anymore

        self._setup_keys(json_keys_dir)
        self._setup_sheep(sheep_class)

        # should probably set self.params
        # before calling setup keys/sheep
        self.params = kwargs


    def _key_is_valid(self, json_key_file):
        """
        Given a JSON file with a bot key,
        check if it is a valid key.
        """
        required_keys = ['consumer_token',
                        'consumer_token_secret',
                        'oauth_token',
                        'oauth_token_secret',
                        'user_id']

        bot_key = {}
        with open(json_key_file,'r') as f:
            bot_key = json.load(f)

        for rk in required_keys:
            if rk not in bot_key.keys():
                return False

        return True


    def _setup_keys(self, json_keys_dir):
        """
        For each json bot key file in the keys directory,
        validate the key, then add it to the list.

        This assumes the key has already been made
        with the Keymaker.
        """
        logger = logging.getLogger('rainbowmindmachine')
        logger.info("Bot Flock Shepherd: Validating keys")
        json_key_files = glob.glob(os.path.join(json_keys_dir, "*.json"))
        for json_key_file in json_key_files:
            if _key_is_valid(json_key_file):
                logger.info("Key %s: VALID")
                self.all_json.append(json_key_file)
            else:
                logger.info("Key %s: INVALID")


    def _setup_sheep(self,sheep_class):
        """
        For each validated json bot key file,
        initialize a Sheep object with that bot key.
        """
        logger = logging.getLogger('rainbowmindmachine')

        MySheepClass = sheep_class
        logger.info("Bot Flock Shepherd: Creating flock %s"%(self.name))

        for jsonf in self.all_json:
            logger.info("Bot Flock Shepherd: Making Sheep for file %s"%(jsonf))
            mysheep = MySheepClass(jsonf)
            self.all_sheep.append(mysheep)

        logger.info("Bot Flock Shepherd: Successfully created flock %s"%(self.name))
        logger.info(its_alive)


    def perform_action(self,action,params={}):
        """
        Perform an action with each bot iteratively.

        Good for things like updating profile information.
        """
        if len(self.all_sheep) > 0:
            for sheep in self.all_sheep:
                sheep.perform_action(action,params)
        else:
            raise Exception("Error: The shepherd has no sheep!")


    def perform_pool_action(self,action,params={}):
        """
        Create a thread pool to perform an action in parallel.

        Good for tweeting, searching, and continuous tasks.
        """

        def do_it(sheep):
            sheep.perform_action(action,params)

        pool = ThreadPool(len(self.all_sheep))
        results = pool.map(do_it,self.all_sheep)

