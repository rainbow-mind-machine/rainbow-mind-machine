import rainbowmindmachine as rmm
import logging


def setup():
    # Make a Rainbow Mind Machine from text files
    k = rmm.TxtKeymaker()
    
    # Run the keymaker to generate a URL the user can use to authenticate/give permission to this app
    k.make_keys('poems/')


def run():
    # keys/ folder contains one file for each sheep, JSON file containing Twitter secret key
    sh = rmm.Shepherd('keys/',sheep_class=rmm.PoemSheep)

    # First, test that the Shepherd can get the flock of Sheep up and running.
    sh.perform_action('echo')

    # Next, we need to test the Sheep ability to construct (and print) tweets from the poem files.
    sh.perform_action('tweet',{'publish':False})

    #sh.perform_pool_action('tweet',{'publish':False})


if __name__=="__main__":
    setup()

