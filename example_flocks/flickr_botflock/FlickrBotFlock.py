import rainbowmindmachine as rmm
import logging


def setup():
    k = rmm.TxtKeymaker()
    k.make_keys('poems/')
    
def run():
    sh = rmm.Shepherd('keys/',sheep_class=rmm.QueneauSheep)

    sh.perform_action('tweet',{'publish':False})
    #sh.perform_pool_action('tweet',{'publish':False})


if __name__=="__main__":
    run()

