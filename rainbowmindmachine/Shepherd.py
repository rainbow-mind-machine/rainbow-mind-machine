import twitter
import os, re, time
import simplejson as json

from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool 

from .Sheep import *
from .Lumberjack import *

alive = r'''
 _______ _______ __ _______      _______ _____   _______ ___ ___ _______ __ __ __
|_     _|_     _|  |     __|    |   _   |     |_|_     _|   |   |    ___|  |  |  |
 _|   |_  |   |  |_|__     |    |       |       |_|   |_|   |   |    ___|__|__|__|
|_______| |___|    |_______|    |___|___|_______|_______|\_____/|_______|__|__|__|
'''

class Shepherd(object):

    def __init__(self, 
                 json_key_dir, 
                 sheep_class=Sheep, 
                 **kwargs):
        """
        Create a Shepherd.

        json_key_dir        Directory where Sheep API keys are located
        sheep_class         Type of Sheep
        kwargs              Logging parameters passed directly to Lumberjack logger

        For example, the Apollo queneau bot is 
        created as follows:

            sh = rmm.Shepherd('keys/',
                              sheep_class = rmm.QueneauSheep,
                              log_file = '/path/to/log')
        """

        # contains each of our sheep
        self.all_sheep = []

        # contains json files with Twitter acct keys
        # (one for each sheep)
        self.all_json = []

        # create the lumberjack instance
        # that all sheep will use to log msgs
        # (parameters checked/enforced by Lumberjack, 
        #  we are just passing them through.)
        self.lumberjack = Lumberjack(**kwargs)

        self._setup_keys(json_key_dir)
        self._setup_sheep(sheep_class)
        self.params = kwargs


    def _setup_keys(self,json_key_dir):
        """
        Set up the Twitter account keys with the Shepherd.

        This assumes keys have already been created by Keymaker. 
        """
        try:
            raw_files = os.listdir(json_key_dir)
        except OSError:
            raise Exception("Error: key directory "+json_key_dir+" does not exist. Have you run the Keymaker?")
        for rfile in raw_files:
            if rfile[-5:] == '.json':
                full_filename = os.path.join(json_key_dir,rfile)
                self.all_json.append(full_filename)

    def _setup_sheep(self,sheep_class):
        """
        Create the Sheep objects (the bot swarm).
        """
        MySheepClass = sheep_class
        self.lumberjack.log("Bot Flock Shepherd: Creating flock")
        for jsonf in self.all_json:
            self.lumberjack.log("Bot Flock Shepherd: Making Sheep for file %s"%jsonf)
            mysheep = MySheepClass(jsonf, self.lumberjack)
            self.all_sheep.append(mysheep)

        self.lumberjack.log(alive)

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

