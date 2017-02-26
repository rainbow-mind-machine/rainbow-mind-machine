import rainbowmindmachine as rmm
from collections import deque
from rainbowmindmachine import QueneauSheep
from queneau import DialogueAssembler
from numpy.random import rand


class WatergateSheep(QueneauSheep):

    def populate_queue(self):
        dialogue = DialogueAssembler.loadlines(open(self.params['file']))
        last_speaker = None

        # Deal more elegantly with speakers.
        messages = []
        speakers = []

        legit_speakers = ['PRESIDENT','EHRLICHMAN','HALDEMANN','KLEINDEIST','HUNT','DEAN','MITCHELL','MCGRUDER','COLSON','KISSINGER','FORD']

        # 100-150 messages
        Nmessages = int(round(50*rand()+100))

        # 2-6 speakers
        Npersons  = int(round(4*rand()+2))

        N = 0
        while N < Nmessages:

            speaker, tokens = dialogue.assemble(last_speaker)

            z = len(speakers)
            if z < Npersons:
                if speaker in legit_speakers:
                    speakers.append(speaker)

            if speaker in speakers:
                last_speaker = speaker
                s = "%s: %s" % (speaker, " ".join(x for x, y in tokens))
                messages.append(s)
                N += 1

        tweet_queue = deque(messages,maxlen=Nmessages)

        return tweet_queue



def setup():
    k = rmm.TxtKeymaker()
    k.make_keys('data/')
    
def run():
    sh = rmm.Shepherd('keys/',sheep_class=WatergateSheep)

    sh.perform_action('tweet',{'publish':False})
    #sh.perform_pool_action('tweet',{'publish':False})

if __name__=="__main__":
    run()

