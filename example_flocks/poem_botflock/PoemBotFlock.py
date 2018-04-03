import rainbowmindmachine as rmm
import logging

"""
Poem Bot Flock Example

This example shows how to create a bot flock 
from a pile of text files (poems).

Put text files into the poems directory.

Run the setup() method once to create the keys,
then run the run() method to fake tweet.

Concepts covered:
    - text file keymaker
    - running bot actions in parallel
"""

def setup():
    # create a keymaker that creates one key per text file
    k = rmm.TxtKeymaker()

    # create keys from text files in poems/
    k.make_keys('poems/')
    
def run():
    # create a shepherd looking for 
    sh = rmm.Shepherd('keys/',sheep_class=rmm.QueneauSheep)

    # test that the Shepherd can get the flock of Sheep up and running.
    sh.perform_action('echo')

    # have all bots tweet in parallel
    sh.perform_pool_action('tweet',{'publish':False})

if __name__=="__main__":
    setup()
    run()
