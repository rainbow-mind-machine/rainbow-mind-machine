import rainbowmindmachine as rmm
import logging

def setup():
    k = rmm.TxtKeymaker()
    k.make_keys('poems/')

def set_img():
    """
    Running perform_action() with the change_image action
    requires each bot to have a change_image param set.
    
    The change_image action takes one parameter, 'image',
    which is the path to the image.
    
    Before we call perform_action(), we have to 
    set the 'image' attritube for each sheep.
    """
    sh = rmm.Shepherd('keys/',
                       sheep_class=rmm.PoemSheep)

    for sheep in sh.all_sheep:
        poem_file = sheep.params['file']
        img_file = re.sub('poems','img',poem_file)
        img_file = re.sub('txt','jpg',img_file)
        sheep.params['image'] = img_file

    # TODO: add set_image perform_action

def tweet():
    sh = rmm.Shepherd('keys/',sheep_class=rmm.PoemSheep)
    sh.perform_pool_action('tweet',{'publish':False})

if __name__=="__main__":
    setup()
    #set_img()
    #tweet()

