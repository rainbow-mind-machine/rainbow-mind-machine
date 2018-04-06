import rainbowmindmachine as rmm

def setup():
    k = rmm.TxtKeymaker()
    k.make_keys('data/')
    
def run():
    sh = rmm.Shepherd('keys/',
                      log_file = 'output.apollo.log',
                      sheep_class = rmm.QueneauSheep)

    # Test performing an action in series
    sh.perform_action('tweet',{'publish':False})

    # Test performing an action in parallel
    sh.perform_pool_action('tweet',{'publish':False})

if __name__=="__main__":
    run()

