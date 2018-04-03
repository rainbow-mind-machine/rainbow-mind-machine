import twitter
import time
import os
import re
import simplejson as json
from numpy.random import rand

from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool 

from Sheep import *


class Shepherd(object):

    def __init__(self,json_key_dir,sheep_class=Sheep):

        # contains each of our sheep
        self.all_sheep = []

        # contains json files with Twitter acct keys
        # (one for each sheep)
        self.all_json = []

        self.setup_keys(json_key_dir)
        self.setup_sheep(sheep_class)


    def setup_keys(self,json_key_dir):
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
                full_filename = re.sub('//','/',json_key_dir + '/' + rfile)
                self.all_json.append(full_filename)

    def setup_sheep(self,sheep_class):
        """
        Create the Sheep objects that represent the 
        Twitter bots.
        """
        MySheepClass = sheep_class
        print("Bot Flock Shepherd: creating flock")
        for jsonf in self.all_json:
            print("Making Sheep for file %s"%jsonf)
            mysheep = MySheepClass(jsonf)
            self.all_sheep.append(mysheep)


    def perform_action(self,action,params={}):
        """
        Perform an action with each bot iteratively.

        Good for things like updating profile information.
        """
        if self.all_sheep<>[]:
            for sheep in self.all_sheep:
                sheep.perform_action( action,params)
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


