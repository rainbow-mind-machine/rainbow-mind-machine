from collections import deque
import logging
from Sheep import Sheep

"""
Extend Sheep behavior to tweet
poems line by line, using poems 
contained in text files.
"""

class PoemSheep(Sheep):
    """
    This class mainly exists to redefine how 
    the tweet queue is populated at the beginning
    of each outer iteration.

    For poems, the process is simple: 
    one line equals one tweet equals one slot in the queue.
    """
    def populate_queue(self):
        """
        Populate a queue of tweets.
        Called by Sheep::tweet()
        """
        # load each line of file into items in a list
        # (the "file" key is set in FilesKeymaker class,
        #  in Keymaker.py)
        with open(self.params['file']) as f:
            lines = f.read().splitlines()

        while '' in lines:
            lines.remove('')

        tweet_queue = deque(lines,maxlen=len(lines))

        msg = self.timestamp_message("Finished populating a new tweet queue with %d tweets."%(len(tweet_queue)))
        logging.info(msg)

        return tweet_queue
    



if __name__=="__main__":

    ### # Do this once
    ### from Keymaker import TxtKeymaker
    ### k = TxtKeymaker()
    ### k.make_keys('poems/')
    
    ### from Shepherd import Shepherd
    ### sh = Shepherd('keys/',sheep_class=PoemSheep)

    ### # First, test that the Shepherd can get the 
    ### # flock of Sheep up and running.
    ### sh.perform_action('echo')

    ### # Next, we need to test the Sheep ability
    ### # to construct (and print) tweets from 
    ### # the poem files.
    ### #sh.perform_action('tweet',{'publish':False})

    ### # Perform the final test: fire up the 
    ### # multi-threaded, multi-headed Twitter
    ### # bot hydra.
    ### # It will construct tweets from poem files
    ### # and send them to the screen or to Twitter.
    ### sh.perform_pool_action('tweet',{'publish':False})

    pass

