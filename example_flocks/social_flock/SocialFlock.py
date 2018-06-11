import rainbowmindmachine as rmm
import logging

class TestSocialSheep(rmm.SocialSheep):
    def populate_queue(self):
        tweet_queue = []
        tweet_queue.append('oh hello again world #rainbowmindmachine')
        tweet_queue.append('you still should not be alarmed #rainbowmindmachine')
        tweet_queue.append('i am still not a bot #rainbowmindmachine')
        return tweet_queue

def setup():
    k = rmm.Keymaker()
    k.set_apikeys_file('apikeys.json')
    k.make_a_key(
            name = 'social_bot',
            json_name = 'social_bot.json',
            keys_out_dir = 'keys'
        )


def tweet():
    sh = rmm.Shepherd( json_keys_dir = 'keys/',
                       flock_name = 'simple flock',
                       sheep_class = TestSocialSheep
                    )

    sh.perform_action('tweet',
            publish = False,
            inner_sleep = 10,
            outer_sleep = 60
    )


def favorite():
    sh = rmm.Shepherd( json_keys_dir = 'keys/',
                       flock_name = 'simple flock',
                       sheep_class = TestSocialSheep
                    )

    sh.perform_action('favorite_toilet',
            sleep = 60,
            search_term = '#rainbowmindmachine'
    )

if __name__=="__main__":
    tweet()

