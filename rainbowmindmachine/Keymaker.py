import urlparse
import oauth2 as oauth
import os
import re
import simplejson as json
import subprocess

try:
    from apikeys import *
except ImportError:
    warning = "Warning: Keymaker was unable to find apikeys.py. This will only be a problem if you are requesting keys."
    print(warning)



class Keymaker(object):
    """
    We do only what we are meant to do.

    Keymaker takes a set of items and asks the user
    if they would like to create a key from each item.

    Keymaker handles the oauth mechanism and does the 
    three-legged authentication dance with Twitter.

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
        try:
            consumer_token = {}
            consumer_token['consumer_token'] = consumer_key
            consumer_token['consumer_token_secret'] = consumer_secret
            self.consumer_token = consumer_token
        except(NameError, KeyError):
            raise Exception("Error: could not read consumer tokens from apikeys.py.")




    def _make_a_key(self,item):
        """
        This private method makes a key for an arbitrary "item"
        (nothing is done with the item).
        """
        item_ = str(item)
        print("="*45)
        print("Item: %s"%(item_))
        print("")

        # (Step 1 is to get a list of items.)

        # Step 2 is to make a Twitter API key for each item.
        make_key = ''
        while make_key is not 'y' and make_key is not 'n':
            make_key = input('Make key? (y/n) ')
        
        if make_key is 'n':
            print("Skipping keymaking for %s"%item_)

            return {}

        else:
            print("Starting keymaking for %s"%item_)

            consumer = oauth.Consumer(consumer_key, consumer_secret)
            client = oauth.Client(consumer)

            # Step 2.1: Get a request token. This is a temporary token that is used for 
            # having the user authorize an access token and to sign the request to obtain 
            # said access token.
            # https://dev.twitter.com/docs/api/1/get/oauth/authenticate
            resp, content = client.request(self.request_token_url,"GET")
            if resp['status'] != '200':
                raise Exception("Invalid response %s. If apikeys.py is present, your keys may be invalid." % resp['status'])

            request_token = dict(urlparse.parse_qsl(content))
            #print("Request Token:")
            #print("    - oauth_token        = %s" % request_token['oauth_token'])
            #print("    - oauth_token_secret = %s" % request_token['oauth_token_secret'])
            #print("")

            # Step 2.2: Redirect to the provider. Since this is a CLI script we do not 
            # redirect. In a web application you would redirect the user to the URL
            # below.
            
            print("Visit the following app authorization link:")
            print("%s?oauth_token=%s" % (self.authorize_url, request_token['oauth_token']))
            print("")
            print("Sign in as the user to be associated with %s"%item_)
            print("")

            # After the user has granted access to you, the consumer, the provider will
            # redirect you to whatever URL you have told them to redirect to. You can 
            # usually define this in the oauth_callback argument as well.
            
            # this should be a 7-digit number
            seven_digit_number = re.compile("[0-9]{7}")
            oauth_verifier = ''
            count = 0
            while not (seven_digit_number.match(oauth_verifier) or oauth_verifier is 'n'):
                if count > 0:
                    print("PIN must be a 7-digit number. Enter 'n' to skip.")
                oauth_verifier = input('What is the PIN? ')
                count += 1

            if oauth_verifier is 'n':

                # party pooper
                return {}
            
            else:

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
                for key in self.consumer_token.keys():
                    d[key] = self.consumer_token[key]

                for key in access_token.keys():
                    d[key] = access_token[key]

                print("Successfully obtained Twitter API key for %s"%item_)

                return d




    def make_a_key(self,item):
        """
        Make a single key.

        If you make bots one item at a time, 
        you are bypassing the normal method of 
        creating multiple bots at a time (bot flock).

        This requires you to specify an item,
        which is a dictionary containing a name for the bot
        and a location for a key file to be created.

        The item dict must contain the keys 'name' and 'json'.

        The key 'name' gives the bot a label.

        The key 'json' indicates the json file where the final key should go.
        """
        if('name' not in item.keys() or 'json' not in item.keys()):
            raise Exception("Error: to use make_a_key, you must specify 'name' and 'json' keys in your input.")

        # TODO:
        # check if these files exist

        d = self._make_a_key(item['name'])

        # store the user's parameter dictionary 
        # together with the Twitter API key
        for key in item.keys():
            d[key] = item[key]

        keys_file = item['json']
        with open(keys_file,'w') as outfile:
            json.dump(d,outfile)

        print("Successfully exported a key bundle for item %s to JSON file %s"%(item['name'],item['json']))



class FilesKeymaker(Keymaker):
    """
    Makes keys by iterating through a directory
    and making a key for each file.
    """
    def __init__(self,extension=''):
        Keymaker.__init__(self)
        self.extension = extension

    def make_keys(self,files_dir,keys_out_dir='keys/'):
        """
        Make multiple keys.

        Go through each file and ask the user, 
        one by one, if they want to make a key for it.

        This bypasses the make_a_key() method
        defined in Sheep, and calls
        _make_a_key() directly.
        """
        # This is the JSON key for the key-value pair 
        # storing the unique file correspoinding to this key.
        # This way, the bot remembers the original file 
        # from which it was created.
        self.file_key = 'file'

        # Step 1
        # Get list of files
        raw_files = os.listdir(files_dir) 
        files = []
        extension = self.extension 
        for rfile in raw_files:

            # if user specifies file extensions,
            # only ask for files with that extension
            # 
            # otherwise, do every file

            if extension is not '':
                el = len(extension)
                elp1 = el+1
                if rfile[-elp1:] is '.'+extension:
                    files.append(rfile)
            else:
                files.append(rfile)

        files.sort()

        # Step 2
        # For each file, ask the user if they want to make a key for it
        consumer_token = self.consumer_token
        for f in files:

            full_file = os.path.join(files_dir,f)

            d = self._make_a_key(full_file)

            if(d is not {}):

                d[self.file_key] = full_file

                # Step 2.5: Export our Sheep key info to a JSON file
                subprocess.call(["mkdir","-p",keys_out_dir])
                full_keys_file = re.sub(files_dir,keys_out_dir,full_file)
                _, ext = os.path.splitext(full_keys_file)

                if(self.extension is ''):
                    keys_file = full_keys_file+".json"
                else:
                    keys_file = re.sub(ext,'.json',full_keys_file)

                with open(keys_file, 'w') as outfile:
                      json.dump(d, outfile)
                print("Successfully exported a key bundle for file %s to JSON file %s"%(full_file, keys_file))



class TxtKeymaker(FilesKeymaker):
    """
    Makes keys by iterating hrough a directory 
    and making a key for each .txt file. 
    """
    def __init__(self):
        FilesKeymaker.__init__(self,extension='txt')


