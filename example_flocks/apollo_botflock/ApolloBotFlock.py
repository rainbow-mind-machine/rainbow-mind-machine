import rainbowmindmachine as rmm

def setup():
    k = rmm.TxtKeymaker()
    k.set_apikeys_file('apikeys.json')
    k.make_keys('data/')
    
def run():
    sh = rmm.Shepherd( json_keys_dir = 'keys/',
                       flock_name = 'simple flock',
                       sheep_class = TestSocialSheep
    )
    sh.perform_action('tweet',
            publish = False
    )

if __name__=="__main__":
    setup()
