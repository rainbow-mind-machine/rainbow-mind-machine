from TwitterAPI import TwitterAPI
import flickr_api
import logging
import requests
import oauth2 as oauth
import os
import os.path
import random
import numpy as np
import simplejson as json
import time
import urllib2 
import httplib
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
from numpy.random import rand
from random import shuffle
from collections import deque
from Sheep import Sheep

try:
    from apikeys import *
except ImportError:
    warning = "Warning: FlickrSheep was unable to find apikeys.py. This will only be a problem if you are requesting keys."
    print warning


# since this is a Flickr photo posting bot,
# let's start by defining a function to get flickr photo links:
def url_for_photo(p):
    url_template = 'http://farm%(farm_id)s.staticflickr.com/%(server_id)s/%(photo_id)s_%(secret)s.jpg'
    return url_template % {
        'server_id': p.get('server'),
        'farm_id': p.get('farm'),
        'photo_id': p.get('id'),
        'secret': p.get('secret'),
    }


"""
Media Sheep

This sheep can upload media.

This uses TwitterAPI library
instead of python-twitter library
because python-twitter library
doesn't allow you to attach
metadata

"""

class MediaSheep(Sheep):

    def perform_action(self,action,params):
        """
        Performs action indicated by string action,
        passing a dictionary of parameters params
        """
        Sheep.perform_action(self,action,params)

        if action=='upload media':
            self.upload_media_to_twitter(params)


    def upload_media_to_twitter(self,params):
        """
        Returns a bundle of information 
        about the media 
        that was uploaded.

        Whoever calls this method
        should take good care 
        of that information.

        Params:

        photo_url : the url of the photo you are uploading to Twitter
        photo_list : the file containing the list of photos we have already uploaded
        """

        # Set up instances of our Token and Consumer. 
        token = oauth.Token(key = self.params['oauth_token'], 
                             secret = self.params['oauth_token_secret'])
        consumer = oauth.Consumer(key = self.params['consumer_token'], 
                                   secret = self.params['consumer_token_secret'])
        client = oauth.Client(consumer,token)


        '''
        uplist = params['photo_list']
        if uplist<>None:

            # First things first:
            # load JSON list of photos we've already uploaded
            # check if we've already uploaded this


            if os.isfile(uplist):

                # if the file exists,
                # load the file
                with open(uplist,'r') as f:
                    d = json.load(f)


            else:

                # the file does not exist,
                # so let's make it



        else:

            # no uploaded photo list provided
            # so upload it regardless

        '''

        photo_url = params['photo_url']

        url = "https://upload.twitter.com/1.1/media/upload.json"

        import urllib

        # download photo to file
        # http://docs.python-requests.org/en/latest/user/quickstart/
        r = requests.get(photo_url)
        (head,tail) = os.path.split(photo_url)
        with open(tail,'w') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)

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
            logging.info(msg)

            ### import pdb; pdb.set_trace()
            ### d['photo_title'] = photo_title
            ### d['photo_id'] = photo_id
            ### d['photo_url'] = photo_url
            ### d['media_id_string'] = media_id_string

        else:

            msg = self.timestamp_message('MEDIA UPLOAD FAILURE')
            logging.info(msg)

        os.remove(tail)

        return d


"""
Flickr Sheep

This sheep can do stuff with the Flickr API.
"""

class FlickrSheep(MediaSheep):

    def perform_action(self,action,params):

        if action=='dummy':
            self.dummy(params)

        elif action=='echo':
            self.echo(params)

        elif action=='change url':
            self.change_url(params)

        elif action=='change bio':
            self.change_bio(params)

        elif action=='change color':
            self.change_color(params)

        elif action=='tweet':
            self.tweet(params)

        elif action=='authorize flickr':
            self.authorize_flickr(params)

    def populate_queue(self):

        # Flickr photos

        flickr_api.set_keys(api_key = flickr_key, api_secret = flickr_secret) 

        # this requires the photobot's name 
        # be the same as the flickr username.
        username = self.params['name']

        user = flickr_api.Person.findByUserName(username)
        photos = user.getPublicPhotos()

        Nphotos = photos.info.total


        # Tweets

        Ntweets = 50

        random_index = range(Ntweets)
        shuffle(random_index)

        for N,ix in zip(random_index,range(Ntweets)):

            results = user.getPhotos(per_page=1,page=ix)
            p = results.data[0]

            url = url_for_photo(p)
            flickr_url = p.getPhotoUrl('Medium')
            title = p.get('title')

            m = self.upload_media_to_twitter({
                    'photo_url' : url
                    })

            # {'image': {'image_type': 'image/jpeg', 'h': 500, 'w': 500}, 'media_id_string': '571761424181035008', 'media_id': 571761424181035008, 'size': 131818}

            f = {}
            f['title'] = title
            f['url'] = url
            f['flickr_url'] = flickr_url

            m['flickr'] = f

            m['tweet'] = title + " " + flickr_url

            messages.append(m)

        tweet_queue = deque(messages,maxlen=Ntweets)

        return tweet_queue


    def _tweet(self,twit):
        """
        twit is a dictionary with some parameters
        """
        url = 'https://api.twitter.com/1.1/statuses/update.json'

        api = TwitterAPI(self.params['consumer_token'],
                         self.params['consumer_token_secret'],
                         self.params['oauth_token'],
                         self.params['oauth_token_secret'])

        media_id = twit['media_id_string']
        twit_text = twit['tweet']

        # media_ids field makes this ia media tweet
        r = api.request('statuses/update',
                {'status': twit_text,
                 'media_ids':media_id})

        if r.status_code == 200:
            msg = self.timestamp_message('UPDATE STATUS SUCCESS')
            msg2 = self.timestamp_message(" > " + twit_text)

            logging.info(msg)
            logging.info(msg2)

        else:
            msg = self.timestamp_message('UPDATE STATUS FAILURE')
            logging.info(msg)


















