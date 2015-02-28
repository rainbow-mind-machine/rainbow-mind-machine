import rainbowmindmachine as rmm
import logging


def setup():
    k = rmm.TxtKeymaker()
    k.make_keys('poems/')
    
def run():
    sh = rmm.Shepherd('keys/',sheep_class=rmm.PoemSheep)

    # # First, test that the Shepherd can get the 
    # # flock of Sheep up and running.
    # sh.perform_action('echo')

    # Next, we need to test the Sheep ability
    # to construct (and print) tweets from 
    # the poem files.
    #sh.perform_action('tweet',{'publish':False})
    sh.perform_pool_action('tweet',{'publish':False})


if __name__=="__main__":
    run()

