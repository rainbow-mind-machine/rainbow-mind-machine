from collections import deque
from random import random
from .Sheep import Sheep
from .queneau import DialogueAssembler

"""
Queneau Sheep

These sheep tweet randomly-assembled 
dialog, generated using queneau assembly.
"""

class QueneauSheep(Sheep):

    def populate_queue(self):
        """
        Populate a queue of tweets.
        Called by Sheep::tweet()
        """
        dialogue = DialogueAssembler.loadlines(open(self.params['file']))
        last_speaker = None

        Nmessages = int(round(5*random()+15))

        messages = []
        for N in range(Nmessages):

            speaker, tokens = dialogue.assemble(last_speaker)
            last_speaker = speaker
            s = "%s: %s" % (speaker, " ".join(x for x, y in tokens))
            messages.append(s)

        tweet_queue = deque(messages,maxlen=Nmessages)

        msg = self.timestamp_message("Finished populating a new tweet queue with %d queneau dialogue tweets."%(len(tweet_queue)))
        self.lumberjack.log(msg)

        return tweet_queue

