import rainbowmindmachine as rmm

class TestSocialSheep(rmm.SocialSheep):
    def populate_queue(self):
        tweet_queue = []
        tweet_queue.append('oh hello again world #rainbowmindmachine')
        tweet_queue.append('you still should not be alarmed #rainbowmindmachine')
        tweet_queue.append('i am still not a bot #rainbowmindmachine')
        return tweet_queue

def setup():
    k = rmm.TwitterKeymaker()
    k.set_apikeys_file('apikeys.json')
    k.make_a_key(
            name = 'social_bot',
            json_name = 'social_bot.json',
            keys_out_dir = 'keys'
        )

def shepherd():
    sh = rmm.TwitterShepherd( 
            json_keys_dir = 'keys/',
            flock_name = 'simple flock',
            sheep_class = TestSocialSheep
    )
    return sh

def tweet():
    sh = shepherd()
    sh.perform_parallel_action(
            'tweet',
            publish = False,
            inner_sleep = 5,
            outer_sleep = 10 
    )

def favorite():
    sh = shepherd()
    sh.perform_parallel_action(
            'favorite',
            sleep = 60,
            search_term = '#rainbowmindmachine'
    )

if __name__=="__main__":
    #setup()
    tweet()
    #favorite()

