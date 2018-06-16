import rainbowmindmachine as rmm

def setup():
    k = rmm.TxtKeymaker()
    k.set_apikeys_file('apikeys.json')
    k.make_keys('data/')
    
def run():
    sh = rmm.Shepherd('keys/',
            sheep_class=rmm.QueneauSheep
    )
    sh.perform_pool_action('tweet',{'publish':False})

if __name__=="__main__":
    setup()
