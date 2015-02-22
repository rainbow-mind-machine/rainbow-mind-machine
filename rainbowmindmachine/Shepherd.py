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

    def __init__(self,json_key_dir):

        # contains each of our sheep
        self.all_sheep = []

        # contains json files with Twitter acct keys
        # (one for each sheep)
        self.all_json = []

        self.setup_keys(json_key_dir)


    def setup_keys(self,json_key_dir):
        """
        Set up the Twitter account keys with the Shepherd.

        This assumes keys have already been created by Keymaker. 
        """
        raw_files = os.listdir(json_key_dir)
        for rfile in raw_files:
            if rfile[-5:] == '.json':
                full_filename = re.sub('//','/',json_key_dir + '/' + rfile)
                self.all_json.append(full_filename)

        print "Bot Flock Shepherd: creating flock"
        for jsonf in self.all_json:
            print "Making Sheep for file "+jsonf
            mysheep = Sheep(jsonf)
            self.all_sheep.append(mysheep)


    def perform_action(self,action,params={}):
        """
        Each Sheep will perform an action 
        sequentially.

        The idea behind this method is to 
        avoid having to define every method
        twice, in the Shepherd and the Sheep.
        """

        for sheep in self.all_sheep:
            sheep.perform_action( action,params)


    def perform_pool_action(self,action,params={}):
        """
        Each Sheep will perform an action
        in parallel.

        The idea behind this method is to 
        avoid having to define every method
        twice, in the Shepherd and the Sheep.
        """

        def do_it(sheep):
            sheep.perform_action(action,params)

        pool = ThreadPool(len(self.all_sheep))
        results = pool.map(do_it,self.all_sheep)


