import rainbowmindmachine as rmm

def setup():
    k = rmm.TxtKeymaker()
    k.set_apikeys_file('apikeys.json')
    k.make_keys('data/')

def shepherd():
    sh = rmm.TwitterShepherd(
            json_keys_dir = 'keys/',
            flock_name = 'apollo space junk bot flock',
            sheep_class = rmm.QueneauSheep
    )
    return sh

def set_url():
    sh = shepherd()
    sh.perform_serial_action(
            'change_url',
            url = 'https://pages.charlesreid1.com/b-apollo/'
    )

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
            search_term = 'Neil Armstrong',
            sleep = 15
    )

if __name__=="__main__":
    #setup()
    #tweet()
    fave()

