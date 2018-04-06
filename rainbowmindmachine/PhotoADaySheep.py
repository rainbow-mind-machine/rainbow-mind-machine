import rainbowmindmachine as rmm
import twitter
import logging
import glob
import time
from datetime import datetime

class PhotoADaySheep(rmm.MediaSheep):
    """
    This sheep will tweet a photo a day.

    This overrides Sheep's default
    inner/outer timing loop and tweet behavior,
    but re-uses a lot of other stuff.

    Constructor takes a dictionary of parameters, 
    stored in self.params


    Parameters:

        images_dir: directory containing images


    Collective actions:
    
        photo_a_day: tweet an image a day
    """
    def perform_action(self,action,params):
        """
        Performs action indicated by string (action),
        passing a dictionary of parameters (params)

        Actions:

            photo_a_day: tweet an image a day
        """
        rmm.Sheep.perform_action(self,action,params)

        if action=='photo_a_day':
            self.photo_a_day(params)



    def populate_queue(self,params):
        """
        Load parameters and prepare the tweet queue.

        This is actually just a list of image files, indexed by 
        the day of the year that they should be tweeted out.

        This method is only called by the public tweet() method.
        """
        # The format of this file can be whatever we'd like.
        # 
        # Opening a json file with contents like 
        #   { "1" : "001.png",
        # seems wasteful.
        # Cut to the chase with glob.
        return glob.glob(params['images_dir']+"/*.jpg")


    def photo_a_day(self,params):
        """
        Tweets an image a day,
        at 8 o'clock or so.

        Parameters:

            upload: boolean, upload media or not

            publish: boolean, publish or not

        """

        # --------------------------
        # Process parameters

        tweet_params = params

        # Default parameter values
        defaults = {}
        defaults['publish'] = False

        # populate missing params with default values
        for dk in defaults.keys():
            if dk not in tweet_params.keys():
                tweet_params[dk] = defaults[dk]


        # --------------------------
        # Start The Calendar

        remcycle = 5

        prior_dd = 0
        while True:

            try:

                # Repopulate in case there are changes
                twit_images = self.populate_queue(tweet_params)
        
                now = datetime.now()
                yy, mm, dd, hh, mm = (now.year, now.month, now.day, now.hour, now.minute)

                # offset for server +8 london time
                offset = 8

                if( abs(dd-prior_dd)>0 and hh>(8 + offset)):

                    # Index = days since beginning of year
                    index = (datetime.now() - datetime(yy,1,1,0,0,0)).days

                    # If there is a photo for this date,
                    if(index < len(twit_images)):

                        # Get photo for this date
                        tweet_params['image_file'] = twit_images[index]

                        img_info = {}

                        # Upload image 
                        if(tweet_params['upload']):
                            img_info = self.upload_image_to_twitter(tweet_params)

                        if(tweet_params['upload'] and tweet_params['publish']):
                            twit = {
                                        'status': 'Your daily Mathematical Tripos question.',
                                        'media_ids': img_info['media_id_string']
                                    }
                            self._tweet(twit)
                        else:
                            self._print("Testing image tweet: %s"%(tweet_params['image_file']))

                    # Update prior_dd
                    prior_dd = dd

                msg = self.timestamp_message("Sleeping...")
                logging.info(msg)

                time.sleep(remcycle)

            except Exception as err:

                # oops!

                msg1 = self.timestamp_message("Sheep encountered an exception. More info:")
                # Fix this:
                msg2 = self.timestamp_message(str(err))
                msg3 = self.timestamp_message("Sheep is continuing...")


                # For debugging:
                raise Exception(err)


                logging.info(msg1)
                logging.info(msg2)
                logging.info(msg3)

                time.sleep(remcycle)

            except AssertionError:
                raise Exception("Error: tweet queue was empty. Check your populate_queue() method definition.")



    def _tweet(self,twit):

        try:
            # tweet:
            stats = self.t.statuses.update(
                    status = twit['status'],
                    media_ids = twit['media_ids']
                    )

            msg = self.timestamp_message(">>> Tweet was successful")

        except twitter.TwitterError as e:
            
            if e.message[0]['code'] == 185:
                msg = self.timestamp_message("Twitter error: Daily message limit reached")
                logging.info(msg)

            elif e.message[0]['code'] == 187:
                msg = self.timestamp_message("Twitter error: Duplicate error")
                logging.info(msg)
            
            else:
                msg = self.timestamp_message("Twitter error: "+e.message)
                logging.info(msg)



