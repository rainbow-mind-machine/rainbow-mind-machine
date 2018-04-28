import urllib
import requests
import oauth
import twitter
import logging
import os, glob, time
from datetime import datetime
from .MediaSheep import MediaSheep

class PhotoADaySheep(MediaSheep):
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
    def perform_action(self,action,params):
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
            self.lumberjack.log(err)
            raise Exception(err)

        # We presume calling perform_action(), the dispatcher method
        # in the parent class, will also pick up methods defined in the
        # child class. We should verify this first, though.
        #Sheep.perform_action(self,action,params)

        # In meantime, hard code:
        # Use the dispatcher method pattern
        if hasattr( self, action ):
            method = getattr( self, action )
            method( params )


    def populate_queue(self, params):
        """
        PhotoADaySheep works slightly differently,
        since it is a multimedia Sheep.

        The populate queue method does not return a list 
        of tweets, it returns a list of image files.

        The photo_a_day() method uploads the image, attaches 
        a message (same each time), and sends off the tweet.

        Parameters:
        -------------

        params contains two keys:
            
            images_dir:         directory containing images
            images_template:    filename pattern, with {i} in place of day of year

        Pass e.g. {i:03} for zero filled integer.

        Example params dictionary:

            { 
                "images_dir" : "puppy_images",
                "images_pattern" : "puppies_{i:03}.jpg"
            }

        TODO:
        ------
        """
        if('images_dir' not in params.keys()):
            err = "Error: no images directory provided to "
            err += "PhotoADaySheep via 'images_dir' parameter"
            self.lumberjack.log(err)
            raise Exception(err)
        if('images_pattern' not in params.keys()):
            err = "Error: no image filename pattern (e.g., \"my_image_{i}.jpg\") "
            err += "were provided to PhotoADaySheep via 'images_template' parameter"
            self.lumberjack.log(err)
            raise Exception(err)

        # This method should load _all_ images,
        # indexed by day of year.
        # 
        # This is kind of stupid, but... sigh...

        image_dir = params['images_dir']
        image_files = []
        for doy in range(366):
            image_file = params['images_pattern'].format(i=doy)

            # don't bother checking if they exist here
            filep = os.path.join(image_dir, image_file)
            image_files.append( filep )
        
        return image_files


    def photo_a_day(self,params):
        """
        Runs forever.
        Tweets an image a day,
        at 8 o'clock or so,
        then goes back to sleep.

        params dictionary settings:

            upload: boolean, upload media or not

            publish: boolean, publish or not

            image_dir: directory containing images

            image_pattern: image file pattern - use {i}

        """

        # --------------------------
        # Process parameters

        # tweet_params contains params for this tweet
        # it starts as a copy of params (tweet <-- sheep),
        # but we'll add more stuff as we go.
        tweet_params = params

        # Default parameter values
        defaults = {}
        defaults['publish'] = False
        defaults['upload'] = False

        # populate missing params with default values
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
                #if( abs(dd-prior_dd)>0 and hh>(hour_to_tweet + offset)):
                if True:

                    # Index = doy of year
                    doy = datetime.now().timetuple().tm_yday

                    # Repopulate in case there are changes
                    twit_images = self.populate_queue(tweet_params)

                    # If there is a photo for this date,
                    if(doy < len(twit_images)):

                        # Get photo for this date
                        tweet_params['image_file'] = twit_images[doy]

                        img_info = {}

                        # Upload image 
                        if(tweet_params['upload']):

                            ###############################################################
                            ####################### fixme #################################
                            img_info = self.upload_image_to_twitter(tweet_params)
                            #
                            # see tinyurl.com/rmm-fixme-link
                            ###############################################################

                        if(tweet_params['upload'] and tweet_params['publish']):
                            twit = {
                                        'status': 'Your daily Mathematical Tripos question.',
                                        'media_ids': img_info['media_id_string']
                                    }
                            self._tweet(twit)
                        else:
                            self._print("Testing image tweet: %s"%(tweet_params['image_file']))

                    else:
                        err = "Warning: for doy = %d, could not find not find "%(doy)
                        err += "the corresponding image %s"%( tweet_params['image_pattern'].format(i=doy) )
                        msg = self.timestamp_message(err)
                        self.lumberjack.log(msg)

                    # Update prior_dd
                    prior_dd = dd

                msg = self.timestamp_message("Sleeping...")
                self.lumberjack.log(msg)

                time.sleep(remcycle)

            except Exception as err:

                # oops!

                msg1 = self.timestamp_message("Sheep encountered an exception. More info:")
                # Fix this:
                msg2 = self.timestamp_message(str(err))
                msg3 = self.timestamp_message("Sheep is continuing...")

                # Add this line in to debug sheep
                raise Exception(err)

                self.lumberjack.log(msg1)
                self.lumberjack.log(msg2)
                self.lumberjack.log(msg3)

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
                self.lumberjack.log(msg)

            elif e.message[0]['code'] == 187:
                msg = self.timestamp_message("Twitter error: Duplicate error")
                self.lumberjack.log(msg)
            
            else:
                msg = self.timestamp_message("Twitter error: "+e.message)
                self.lumberjack.log(msg)

    def upload_image_to_twitter(self, params):

        # Set up instances of our Token and Consumer.
        token = oauth.Token(key = params['oauth_token'],
                            secret = params['oauth_token_secret'])

        consumer = oauth.Consumer(key = params['consumer_token'],
                                  secret = params['consumer_token_secret'])

        client = oauth.Client(consumer,token)

        url = "https://upload.twitter.com/1.1/media/upload.json"

        imgfile = params['image_file']

        # Generate multipart data and headers from content
        datagen, headers = multipart_encode({'media': open(imgfile,'rb')})

        req = oauth.Request.from_consumer_and_token(
                consumer, 
                token=token, 
                http_url=url,
                parameters=None, 
                http_method="POST")

        req.sign_request(oauth.SignatureMethod_HMAC_SHA1(), consumer, token)

        # Generate multipart data and headers from content
        datagen, headers = multipart_encode({'media': open(tail,'rb')})

        # Body to string
        body = "".join(datagen)

        # Create the request 
        resp, content = client.request(
                    url,
                    method = "POST",
                    body=body,
                    headers=headers
                    )

                d = {}

        if resp['status']=='200':

            # we have our media id string!

            d = json.loads(content)
            ### media_id_string = c['media_id_string']
            ### media_id = c['media_id']

            msg = self.timestamp_message('MEDIA UPLOAD SUCCESS')
            self.lumberjack.log(msg)
            self.lumberjack.log("%s"%(d))

        else:

            msg = self.timestamp_message('MEDIA UPLOAD FAILURE')
            self.lumberjack.log(msg)

        return d

