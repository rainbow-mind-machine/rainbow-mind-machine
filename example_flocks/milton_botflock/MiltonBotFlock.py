import rainbowmindmachine as rmm
import os, re
from os.path import join

def setup():
    k = rmm.TxtKeymaker()
    k.set_apikeys_file('apikeys.json')
    k.make_keys('poems/')

def shepherd():
    sh = rmm.Shepherd(
            json_keys_dir = 'keys/',
            flock_name = 'paradise lost bot flock',
            sheep_class = rmm.PoemSheep
    )
    return sh

def img():
    """
    change_image action requires an 'image' kwarg.
    """
    sh = shepherd()

    for sheep in sh.flock:
        poem_file = sheep.params['file']
        img_file = re.sub('poems','img',poem_file)
        img_file = re.sub('txt','jpg',img_file)
        sheep.params['image'] = img_file

    sh.perform_serial_action('change_image')

def tweet():
    sh = rmm.Shepherd('keys/',sheep_class=rmm.PoemSheep)
    sh.perform_parallel_action(
            'tweet',
            publish = False
    )

if __name__=="__main__":
    setup()
    #img()
    #tweet()

