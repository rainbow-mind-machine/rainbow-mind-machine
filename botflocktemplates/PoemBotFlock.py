import rainbowmindmachine as rmm

from collections import deque
import logging

"""
Extend Sheep behavior to tweet
poems line by line, using poems 
contained in text files.
"""

#class PoemSheep(Sheep):
#    """
#    This class mainly exists to redefine how 
#    the tweet queue is populated at the beginning
#    of each outer iteration.
#
#    For poems, the process is simple: 
#    one line equals one tweet equals one slot in the queue.
#
#    The TxtKeymaker saves 
#    """
#    def populate_queue(self):
#        """
#        Populate a queue of tweets.
#        Called by Sheep::tweet()
#        """
#        # load each line of file into items in a list
#        # (the "file" key is set in FilesKeymaker class,
#        #  in Keymaker.py)
#        with open(self.params['file']) as f:
#            lines = f.read().splitlines()
#
#        tweet_queue = deque(lines,maxlen=len(lines))
#
#        msg = self.timestamp_message("Finished populating a new tweet queue with %d tweets."%(len(tweet_queue)))
#        logging.info(msg)
#
#        return tweet_queue



def main():

    ## Do this once
    #k = rmm.TxtKeymaker()
    #k.make_keys('poems/')
    
    sh = rmm.Shepherd('keys/',sheep_class=rmm.PoemSheep)

    ### # First, test that the Shepherd can get the 
    ### # flock of Sheep up and running.
    ### sh.perform_action('echo')

    # Next, we need to test the Sheep ability
    # to construct (and print) tweets from 
    # the poem files.
    sh.perform_action('tweet',{'publish':False})
    #sh.perform_pool_action('tweet',{'publish':False})


if __name__=="__main__":
    main()

