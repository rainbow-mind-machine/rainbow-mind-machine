from collections import deque
import logging
from .Sheep import Sheep

"""
Poem Sheep

These sheep tweet poems, one line at a time.
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

        msg = self.timestamp_message("Finished populating a new tweet queue with %d poem tweets."%(len(tweet_queue)))
        logging.info(msg)

        return tweet_queue

