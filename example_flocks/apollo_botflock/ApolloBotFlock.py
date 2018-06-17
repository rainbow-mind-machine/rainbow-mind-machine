import rainbowmindmachine as rmm

def setup():
    k = rmm.TxtKeymaker()
    k.set_apikeys_file('apikeys.json')
    k.make_keys('data/')
    
def run():
    sh = rmm.Shepherd( json_keys_dir = 'keys/',
                       flock_name = 'apollo space junk bot flock',
                       sheep_class = rmm.QueneauSheep
    )
    sh.perform_parallel_action('tweet',
            publish = False
    )

if __name__=="__main__":
    #setup()
    run()
