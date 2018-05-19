import urllib
import requests
import oauth2 as oauth
import twitter
import logging
import os, glob, time
from datetime import datetime
from .Sheep import Sheep

class PhotoADaySheep(Sheep):
    """
    This sheep will tweet a photo a day.

    This overrides Sheep's default
    inner/outer timing loop and tweet behavior,
    but re-uses a lot of other stuff.

    Constructor takes a dictionary of parameters, 
    stored in self.params


    Parameters:

        images_dir: directory containing images

        images_template: string template of image names, 
                letting {i} represent zero-filled integer
                day of the year (1 to 366). 
                Example: puppies_{i}.jpg

    Collective actions:
    
        photo_a_day: tweet an image a day
    """
    def perform_action(self,action,extra_params):
        """
        Performs action indicated by string (action),
        passing a dictionary of parameters (params).

        The user should not call tweet() directly
        for the PhotoADaySheep, they should call
        photo_a_day() instead.

        Available (additional) actions:
        - photo_a_day
        """
        if(action=='tweet'):
            err = "Error: Do not call the 'tweet' action on "
            err += "PhotoADaySheep directly. Call the 'photo_a_day' "
            err += "action instead."
            raise Exception(err)

        # Use the dispatcher method pattern
        if hasattr( self, action ):
            method = getattr( self, action )
            method( extra_params )


    def populate_queue(self, extra_params):
        """
        PhotoADaySheep works slightly differently,
        since it is a multimedia Sheep.

        The populate queue method does not return a list 
        of tweets, it returns a list of image files.

        The photo_a_day() method uploads the image, attaches 
        a message (same each time), and sends off the tweet.

        Parameters:
        -------------

        extra_params contains two keys:
            
            images_dir:         directory containing images
            images_template:    filename pattern, with {i} in place of day of year

        Pass e.g. {i:03} for zero filled integer.

        Example extra_params dictionary:

            { 
                "images_dir" : "puppy_images",
                "images_pattern" : "puppies_{i:03}.jpg"
            }

        TODO:
        ------
        """
        if('images_dir' not in extra_params.keys()):
            err = "Error: no images directory provided to "
            err += "PhotoADaySheep via 'images_dir' parameter"
            raise Exception(err)
        if('images_pattern' not in extra_params.keys()):
            err = "Error: no image filename pattern (e.g., \"my_image_{i}.jpg\") "
            err += "were provided to PhotoADaySheep via 'images_template' parameter"
            raise Exception(err)

        # This method should load _all_ images,
        # indexed by day of year.
        # 
        # This is kind of stupid, but... sigh...

        image_dir = extra_params['images_dir']
        image_files = []
        for doy in range(366):
            image_file = extra_params['images_pattern'].format(i=doy)

            # don't bother checking if they exist here
            filep = os.path.join(image_dir, image_file)
            image_files.append( filep )
        
        return image_files


    def photo_a_day(self,tweet_params):
        """
        Runs forever.
        Tweets an image a day,
        at 8 o'clock or so,
        then goes back to sleep.

        tweet_params dictionary settings:

            publish: boolean, publish or not

            image_dir: directory containing images

            image_pattern: image file pattern - use {i}

        """

        # --------------------------
        # Process parameters

        # tweet_params contains parameters for this tweet

        # Default parameter values
        defaults = {}
        defaults['publish'] = False

        # populate missing parameters with default values
        for dk in defaults.keys():
            if dk not in tweet_params.keys():
                tweet_params[dk] = defaults[dk]


        # --------------------------
        # Start The Calendar
        # 
        # Granted, this is a bit more complicated 
        # than it could be, but it's relatively simple,
        # and if it ain't broke, don't fix it.

        logger = logging.getLogger('rainbowmindmachine')

        remcycle = 120 # sleep (in seconds)

        prior_dd = 0
        while True:

            try:

                now = datetime.now()
                yy, mm, dd, hh, mm = (now.year, now.month, now.day, now.hour, now.minute)

                # the time will always be zulu in a docker container, +8 hr offset
                offset = 8

                hour_to_tweet = 8
                if( abs(dd-prior_dd)>0 and hh>(hour_to_tweet + offset)):

                    # Index = doy of year
                    doy = datetime.now().timetuple().tm_yday

                    # Repopulate in case there are changes
                    twit_images = self.populate_queue(tweet_params)

                    # If there is a photo for this date,
                    if(doy < len(twit_images)):

                        # Get photo for this date
                        media_attachment = twit_images[doy]

                        try:
                            twit = tweet_params['message']

                        except KeyError:
                            err = "Warning: could not find a message, using hello world"
                            msg = self.timestamp_message(err)
                            logger.info(msg)

                            twit = 'Hello world'

                        if(tweet_params['publish']):
                            self._tweet(twit, media=media_attachment)
                        else:
                            self._print("Testing image tweet: %s"%(media_attachment))

                    else:
                        err = "Warning: for doy = %d, could not find not find "%(doy)
                        err += "the corresponding image %s"%( tweet_params['image_pattern'].format(i=doy) )
                        msg = self.timestamp_message(err)
                        logger.info(msg)

                    # Update prior_dd
                    prior_dd = dd

                msg = self.timestamp_message("Sleeping...")
                logger.info(msg)

                time.sleep(remcycle)

            except Exception as err:

                # oops!

                msg1 = self.timestamp_message("Sheep encountered an exception. More info:")
                # Fix this:
                msg2 = self.timestamp_message(str(err))
                msg3 = self.timestamp_message("Sheep is continuing...")

                # Add this line in to debug sheep
                #raise Exception(err)

                logger.info(msg1)
                logger.info(msg2)
                logger.info(msg3)

                time.sleep(remcycle)

            except AssertionError:
                raise Exception("Error: tweet queue was empty. Check your populate_queue() method definition.")

