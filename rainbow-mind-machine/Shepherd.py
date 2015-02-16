import twitter
import time
import os
import simplejson as json
from numpy.random import rand

class Shepherd(object):

    def __init__(self):

        # contains each of our sheep
        self.all_sheep = []

        # contains json files with Twitter acct keys
        # (one for each sheep)
        self.all_json = []

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

    def perform_action(self,action,**kwargs):
        """
        Perform an action on each Sheep.

        This does its best to pass the 
        action and its parameters
        striaght through to each Sheep.

        This avoids having to define separate
        methods for each action, in the Shepherd
        and in the Sheep.

        Actually tweeting or test tweeting
        is a special case, because it goes on
        indefinitely. In this case,
        a multithread pool is created
        so that each Sheep can run in parallel.

        In every other case, we iterate through
        each sheep and perform the desired
        action, one Sheep at a time.
        """

        if action=='tweet':

            def do_it(sheep):
                sheep.tweet()

            pool = ThreadPool(len(self.all_sheep))
            results = pool.map(do_it,self.all_sheep)

        elif action=='echo':

            def do_it(sheep):
                sheep.echo()

            pool = ThreadPool(len(self.all_sheep))
            results = pool.map(do_it,self.all_sheep)

        else:
            for sheep in self.all_sheep:
                sheep.perform_action( action, **kwargs )



