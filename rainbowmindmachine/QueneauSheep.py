from .SocialSheep import SocialSheep
from .queneau import DialogueAssembler
from random import random

from .utils import eprint

"""
Queneau Sheep

These sheep tweet randomly-assembled 
dialog, generated using queneau assembly.
"""

class QueneauSheep(SocialSheep):

    def populate_tweet_queue(self):
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

        tweet_queue = messages

        msg = "rainbow-mind-machine: QueneauSheep: Finished populating a new tweet queue with %d queneau dialogue tweets."%(len(tweet_queue))
        eprint(msg)

        return tweet_queue

