import rainbowmindmachine as rmm

def setup():
    k = rmm.TxtKeymaker()
    k.set_apikeys_file('apikeys.json')
    k.make_keys('poems/')

def shepherd():
    sh = rmm.Shepherd(
            json_keys_dir = 'keys/',
            flock_name = 'ginsberg bot flock',
            sheep_class = rmm.PoemSheep
    )
    return sh
    
def tweet():
    sh = shepherd()
    sh.perform_parallel_action(
            'tweet',
            publish = False
    )

def fave():
    sh = shepherd()
    sh.perform_parallel_action(
            'favorite',
            search_term = 'Allen Ginsberg',
            sleep = 15
    )

if __name__=="__main__":
    #setup()
    #tweet()
    fave()

