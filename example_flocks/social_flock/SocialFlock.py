import rainbowmindmachine as rmm
import logging

def setup():
    k = rmm.Keymaker()
    k.set_apikeys_file('apikeys.json')
    k.make_a_key(
            name = 'social_bot',
            json_name = 'social_bot.json',
            keys_out_dir = 'keys'
        )
    
def run():
    sh = rmm.Shepherd( json_keys_dir = 'keys/',
                       flock_name = 'simple flock',
                       sheep_class = rmm.SocialSheep
                    )
    sh.perform_action('tweet',{'publish':False})
    #sh.perform_pool_action('tweet',{'publish':False})

if __name__=="__main__":
    run()
