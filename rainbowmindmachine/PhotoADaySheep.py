from .SocialSheep import SocialSheep
import traceback
import urllib
import requests
import oauth2 as oauth
import twitter
import logging
import os, glob, time
from datetime import datetime
from .TwitterSheep import TwitterSheep

from .utils import eprint

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
            err = "Error: Do not call the 'tweet' action on "
            err += "PhotoADaySheep directly. Call the 'photo_a_day' "
            err += "action instead."
            logging.error(err)
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
            raise Exception(err)
        if('images_pattern' not in extra_params.keys()):
            err = "Error: no image filename pattern (e.g., \"my_image_{i}.jpg\") "
            err += "were provided to PhotoADaySheep via 'images_template' parameter"
            logging.error(err)
            raise Exception(err)

        # This method should load _all_ images
                    prior_dd = dd

                msg = self.timestamp_message("PhotoADaySheep: photo_a_day(): Sleeping...")
                logging.error(msg)

                time.sleep(remcycle)

            except Exception as err:

                # oops!

                msg1 = self.timestamp_message("PhotoADaySheep: photo_a_day(): Encountered an exception. More info:")
                msg2 = self.timestamp_message(traceback.format_exc())
                msg3 = self.timestamp_message("PhotoADaySheep: photo_a_day(): Continuing...")

                # Add this line in to debug sheep
                #raise Exception(err)

                logging.error(msg1)
                logging.error(msg2)
                logging.error(msg3)

                time.sleep(remcycle)

            except AssertionError:
                raise Exception("Error: tweet queue was empty. Check your populate_queue() method definition.")

