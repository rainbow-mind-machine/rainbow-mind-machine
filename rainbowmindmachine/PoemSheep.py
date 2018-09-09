from .TwitterSheep import TwitterSheep
import logging

"""
Poem Sheep

These sheep tweet poems, one line at a time.
"""

class PoemSheep(TwitterSheep):
    """
    This class mainly exists to redefine how 
    the tweet queue is populated at the beginning
    of each outer iteration.

    For poems, the process is simple: 
    one line equals one tweet equals one slot in the queue.
    """
    def populate_tweet_queue(self):
        """
        Populate a queue of tweets.
        Called by TwitterSheep::tweet()
        """
        # load each line of file into items in a list
        # (the "file" key is set by the FilesKeymaker class)
        logging.debug(self.params)
        with open(self.params['file']) as f:
            lines = f.read().splitlines()

        while '' in lines:
            lines.remove('')

        tweet_queue = list(lines)

        msg = "PoemSheep: populate_tweet_queue(): Finished populating a new tweet queue with %d poem tweets."%(len(tweet_queue))
        logging.debug(self.sign_message(msg))

        return tweet_queue

