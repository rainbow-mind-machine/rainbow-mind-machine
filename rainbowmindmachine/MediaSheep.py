from .SHeep import Sheep

class MediaSheep(Sheep):

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


