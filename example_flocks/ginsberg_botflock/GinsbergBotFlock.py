import rainbowmindmachine as rmm

def setup():
    k = rmm.TxtKeymaker()
    k.set_apikeys_file('apikeys.json')
    k.make_keys('poems/')
    
def run():
    sh = rmm.Shepherd( json_keys_dir = 'keys/',
                       flock_name = 'ginsberg bot flock',
                       sheep_class = PoemSheep
    )
    sh.perform_action('tweet',
            publish = False
    )

if __name__=="__main__":
    setup()
