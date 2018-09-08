from .SocialSheep import SocialSheep
import logging
import urllib
import requests
import oauth2 as oauth
import twitter
import logging
import os, glob, time
from datetime import datetime
from .TwitterSheep import TwitterSheep


class PhotoADaySheep(TwitterSheep):
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
            err = "PhotoADaySheep: perform_action(): Do not call the 'tweet' action on "
            err += "PhotoADaySheep directly. Call the 'photo_a_day' "
            err += "action instead."
            logging.error(err, exc_info=True)
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
            logging.error(err)
            raise Exception(err, exc_info=True)
        if('images_pattern' not in extra_params.keys()):
            err = "Error: no image filename pattern (e.g., \"my_image_{i}.jpg\") "
            err += "were provided to PhotoADaySheep via 'images_template' parameter"
            logging.error(err)
            raise Exception(err, exc_info=True)

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

                    msg = "PhotoADaySheep: photo_a_day(): Time to tweet.\n"
                    msg += "    day of the year = %d"%(doy)
                    msg += "    num of images   = %d"%(len(twit_images))
                    if(doy < len(twit_images)):
                        msg += "    we found a photo"
                    else:
                        msg += "    no photo to tweet"
                    logging.debug(msg)

                    # If there is a photo for this date,
                    if(doy < len(twit_images)):

                        # Get photo for this date
                        media_attachment = twit_images[doy]

                        try:
                            twit = tweet_params['message']
                        except KeyError:
                            twit = 'Hello world'

                        msg = "PhotoADaySheep: photo_a_day(): tweeting the twit \"%s\""%(twit)
                        logging.debug(msg)

                        if(tweet_params['publish']):
                            self._tweet(twit, media=media_attachment)
                        else:
                            msg = "PhotoADaySheep: photo_a_day(): Testing image tweet: %s"%(media_attachment)
                            logging.info(msg)

                    else:
                        msg = "PhotoADaySheep Warning: photo_a_day(): for doy = %d, could not find not find "%(doy)
                        msg += "the corresponding image %s"%( tweet_params['image_pattern'].format(i=doy) )
                        logging.error(msg)

                    # Update prior_dd
                    prior_dd = dd

                msg = "PhotoADaySheep: photo_a_day(): Sleeping..."
                logging.debug(msg)

                time.sleep(remcycle)

            except Exception as err:

                # oops!

                msg1 = "PhotoADaySheep: photo_a_day(): Encountered an exception. More info:"
                msg2 = traceback.format_exc()
                msg3 = "Sheep is continuing..."

                # Add this line in to debug sheep
                #raise Exception(err)

                logging.error(msg1)
                logging.error(msg2)
                logging.error(msg3)

                time.sleep(remcycle)

            except AssertionError:

                err = "TwitterSheep Error: tweet(): tweet queue was empty. Check your populate_tweet_queue() method definition."
                logging.error(err)
                raise Exception(err)


