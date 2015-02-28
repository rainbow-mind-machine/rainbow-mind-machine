import rainbowmindmachine as rmm
import logging


def setup():
    k = rmm.Keymaker()
    k.make_a_key({
        'name' : 'cmrhipstamatic',
        'json' : 'keys/cmrhipstamatic.json'
        })

def run():
    sh = rmm.Shepherd('keys/',sheep_class=rmm.FlickrSheep)

    sh.perform_action('tweet',{'publish':False})
    a = 0
    #sh.perform_pool_action('tweet',{'publish':False})


if __name__=="__main__":
    run()

