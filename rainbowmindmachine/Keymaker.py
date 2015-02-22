import urlparse
import oauth2 as oauth
import os
import re
import simplejson as json

from apikeys import *

class Keymaker(object):
    """
    We do only what we are meant to do.

    Keymaker handles the oauth mechanism
    and does three-legged authentication.

    This results in one public/private key pair per sheep.
    With a sheep's keys, you can tweet as that sheep.
    """
    def __init__(self):
        # We won't do much here
        self.request_token_url = 'https://api.twitter.com/oauth/request_token'
        self.authorize_url = 'https://api.twitter.com/oauth/authorize'
        self.access_token_url = 'https://api.twitter.com/oauth/access_token'

        # apikeys.py defines
        # consumer_key
        # consumer_secret
        consumer_token = {}
        consumer_token['consumer_token'] = consumer_key
        consumer_token['consumer_token_secret'] = consumer_secret
        self.consumer_token = consumer_token

    def make_keys(self,poems_dir):
        """
        Go through each poem and ask the user, 
        one by one, if they want to make a key for it.
        """
        # 1. Get list of poem files
        raw_files = os.listdir(poems_dir) 
        poem_files = []
        for rfile in raw_files:
            if rfile[-4:] == '.txt':
                poem_files.append(rfile)

        # 2. For each poem, ask the user if they want to make a key for it
        consumer_token = self.consumer_token
        for poem_file in poem_files:

            full_poem_file = re.sub('//','/',poems_dir + '/' + poem_file)

            print "="*45
            print "Poem "+full_poem_file
            print 
            make_key = ''
            while make_key <> 'y' and make_key <> 'n':
                make_key = raw_input('Make key? (y/n) ')
            
            if make_key == 'n':
                print "Skipping keymaking for poem "+full_poem_file
            else:
                print "Starting keymaking for poem "+full_poem_file

                consumer = oauth.Consumer(consumer_key, consumer_secret)
                client = oauth.Client(consumer)

                # Step 2.1: Get a request token. This is a temporary token that is used for 
                # having the user authorize an access token and to sign the request to obtain 
                # said access token.
                # https://dev.twitter.com/docs/api/1/get/oauth/authenticate
                resp, content = client.request(self.request_token_url,"GET")
                if resp['status'] != '200':
                    raise Exception("Invalid response %s." % resp['status'])

                request_token = dict(urlparse.parse_qsl(content))
                #print "Request Token:"
                #print "    - oauth_token        = %s" % request_token['oauth_token']
                #print "    - oauth_token_secret = %s" % request_token['oauth_token_secret']
                #print 

                # Step 2.2: Redirect to the provider. Since this is a CLI script we do not 
                # redirect. In a web application you would redirect the user to the URL
                # below.
                
                print "Visit the following app authorization link:"
                print "%s?oauth_token=%s" % (self.authorize_url, request_token['oauth_token'])
                print 
                print "Sign in as the user to be associated with poem "+full_poem_file
                print 

                # After the user has granted access to you, the consumer, the provider will
                # redirect you to whatever URL you have told them to redirect to. You can 
                # usually define this in the oauth_callback argument as well.
                oauth_verifier = raw_input('What is the PIN? ')

                # Step 2.3: Once the consumer has redirected the user back to the oauth_callback
                # URL you can request the access token the user has approved. You use the 
                # request token to sign this request. After this is done you throw away the
                # request token and use the access token returned. You should store this 
                # access token somewhere safe, like a database, for future use.
                token = oauth.Token(request_token['oauth_token'],
                    request_token['oauth_token_secret'])
                token.set_verifier(oauth_verifier)
                client = oauth.Client(consumer, token)
                
                resp, content = client.request(self.access_token_url, "POST")
                access_token = dict(urlparse.parse_qsl(content))

                # Step 2.4: Make a dict with all relevant Sheep info
                d = {}
                for key in consumer_token.keys():
                    d[key] = consumer_token[key]
                for key in access_token.keys():
                    d[key] = access_token[key]
                d['poem_file'] = full_poem_file
                
                # Step 2.5: Export our Sheep key info to a JSON file
                full_keys_file = re.sub('poems','keys',full_poem_file)
                keys_file = re.sub('txt','json',full_keys_file)
                with open(keys_file, 'w') as outfile:
                      json.dump(d, outfile)
                print "Successfully exported a key bundle for poem "+full_poem_file+" to JSON file "+ keys_file 

if __name__=="__main__":
    km = Keymaker()
    km.make_keys('poems/')
