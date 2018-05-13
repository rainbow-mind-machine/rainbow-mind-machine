import urllib
import oauth2 as oauth
import os, re, glob
import json
import subprocess
from os.path import isfile, isdir, exists
from os.path import join, basename, splitext


class Keymaker(object):
    """
    We do only what we are meant to do.

    Keymaker takes a set of items and asks the user
    if they would like to create a key from each item.

    Keymaker handles the oauth mechanism and does the 
    three-legged authentication dance with Twitter.

    This results in one public/private key pair per sheep.
    With a sheep's keys, you can tweet as that sheep.

    (NOTE: Keymaker does not use Lumberjack, 
    Lumberjack is for the flock only.)
    """
    def __init__(self):
        # We won't do much here
        self.request_token_url = 'https://api.twitter.com/oauth/request_token'
        self.authorize_url = 'https://api.twitter.com/oauth/authorize'
        self.access_token_url = 'https://api.twitter.com/oauth/access_token'
        
        self.apikeys_set = False

    # 
    # 
    # Load Application (Consumer) API Keys
    # 
    #

    def set_apikeys_env(self):
        """
        Set the API keys using environment variables:

            $CONSUMER_TOKEN
            $CONSUMER_TOKEN_SECRET
        """
        if( os.environ['CONSUMER_TOKEN'] and os.environ['CONSUMER_TOKEN_SECRET'] ):
            self.consumer_token = {}
            self.consumer_token['consumer_token'] = os.environ['CONSUMER_TOKEN']
            self.consumer_token['consumer_token_secret'] = os.environ['CONSUMER_TOKEN']
            self.apikeys_set = True
        else:
            raise Exception("Error: environment variables CONSUMER_TOKEN and CONSUMER_TOKEN_SECRET were not set.")


    def set_apikeys_file(self,f_apikeys):
        """
        Set the API keys using an external JSON file
        with the keys:

            consumer_token
            consumer_token_secret
        """
        if( not exists(f_apikeys) ):
            # Nope, no idea
            raise Exception("Error: could not find specified apikeys file %s"%(f_apikeys))

        elif( not isfile(f_apikeys) ):

            # user specified a directory.
            # check if it contains apikeys.json
            f_apikeys = join(f_apikeys,'apikeys.json')
            if( not isfile( f_apikeys ) ):
                raise Exception("Error: could not find specified apikeys file %s"%(f_apikeys))

        try:
            with open(f_apikeys,'r') as f:
                d = json.load(f)
        except (json.errors.JSONDecodeError):
            raise Exception("Error: given file %s is not valid JSON"%(f_apikeys))
        
        self.set_apikeys_dict(d)


    def set_apikeys_dict(self,d_apikeys):
        """
        Set the API keys by passing a dictionary
        with the keys

            consumer_token
            consumer_token_secret
        """
        ct = ['consumer_token','consumer_token_secret']
        try:
            self.consumer_token = {}
            for k in ct:
                self.consumer_token[k] = d_apikeys[k]

            self.apikeys_set = True

        except(NameError, KeyError):
            err = "Error: could not set API keys, invalid keys provided.\n\n"
            err += "Expected: %s\n\n"%(", ".join(ct))
            err += "Received: %s\n\n"%(", ".join(d_apikeys.keys()))
            raise Exception(err)


    # 
    # 
    # Make Bot OAuth Keys
    # 
    #

    def make_a_key( self, 
                    name, json,
                    keys_out_dir='keys/', 
                    interactive=True):
        """
        Public method to make a single key from a single item.

        If you make bots one item at a time, 
        you are bypassing the "normal" method of 
        creating multiple bots at a time (bot flock),
        so you must specify an item.

            name :          Label for the bot

            json :          The name of the JSON file in which to save
                            the bot OAuth key (all paths are ignored).

            keys_out_dir :  Directory in which to place final JSON keys
                            containing OAuth tokens and other bot info

            interactive :   Go through the interactive three-legged OAuth process
                            (only set to False for testing)
        """
        # Step 1:
        # Get a private key to tweet as this user,
        # and if ok, populate with this item's details

        d = self._make_a_key(name, interactive=interactive)

        if(d != {}):

            # Store the item data passed in
            # together with the Twitter API key
            for key in item.keys():
                d[key] = item[key]

            # Step 2:
            # Export the bot data bundle to a json file
            # in the keys directory.
            # Ignore any prefix the user provides 
            # and just grab the basename of the json file.

            # Make a key dir
            subprocess.call(["mkdir","-p",keys_out_dir])

            keys_file = basename(json)
            keys_out = join(keys_out_dir,keys_file)

            with open(keys_out,'w') as outfile:
                json.dump(d,outfile)

            print("Successfully exported a key bundle for item %s to JSON file %s"%(name,keys_out))

        else:
            # If we run non-interactively (test),
            # this is what we will get
            print("Did not export a key bundle for item %s (no auth step!)"%(name))




    def _make_a_key(self, item, interactive=True):
        """
        This private method makes a key for an arbitrary "item"
        (nothing is done with the item).

        If interactive=False, this simply passes through. 
        """
        if(not self.apikeys_set):
            err = "Error: API keys were not set for the Shepherd."
            raise Exception(err)

        item_ = str(item)
        print("="*45)
        print("Item: %s"%(item_))
        print("")

        # (Step 1 is to get a list of items.)

        # Step 2 is to make a Twitter API key for each item.
        if not interactive:
            return {}

        make_key = ''
        while make_key != 'y' and make_key != 'n':
            make_key = input('Make key? (y/n) ')
            
        if make_key=='n':
            print("Skipping keymaking for %s"%item_)

            return {}

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

        request_token = dict(urllib.parse.parse_qsl(content))
        oauth_token = request_token[b'oauth_token'].decode('utf-8')
        oauth_token_secret = request_token[b'oauth_token_secret'].decode('utf-8')

        print("Request Token:")
        print("    - oauth_token        = %s" % oauth_token)
        print("    - oauth_token_secret = %s" % oauth_token_secret)
        print("")

        # Step 2.2: Redirect to the provider. Since this is a CLI script we do not 
        # redirect. In a web application you would redirect the user to the URL
        # below.

        print("Visit the following app authorization link:")
        print("%s?oauth_token=%s" % (self.authorize_url, oauth_token ))
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
        while not (seven_digit_number.match(oauth_verifier) or oauth_verifier == 'n'):
            if count > 0:
                print("PIN must be a 7-digit number. Enter 'n' to skip or 'r' to renew the link.")
            oauth_verifier = input('What is the PIN? ')
            count += 1

        if oauth_verifier == 'n':

            # party pooper
            return {}

        elif oauth_verifier == 'r':

            # go through the oauth dance again
            self.make_a_key(item)
        
        else:

            # Step 2.3: Once the consumer has redirected the user back to the oauth_callback
            # URL you can request the access token the user has approved. You use the 
            # request token to sign this request. After this is done you throw away the
            # request token and use the access token returned. You should store this 
            # access token somewhere safe, like a database, for future use.
            oauth_token = request_token[b'oauth_token'].decode('utf-8')
            oauth_token_secret = request_token[b'oauth_token'].decode('utf-8')
            token = oauth.Token(oauth_token, oauth_token_secret)

            token.set_verifier(oauth_verifier)
            client = oauth.Client(consumer, token)
            
            resp, content = client.request(self.access_token_url, "POST")
            access_token = dict(urllib.parse.parse_qsl(content))

            # Step 2.4: Make a dict with all relevant Sheep info
            d = {}
            for key in self.consumer_token.keys():
                d[key] = self.consumer_token[key]

            for key in access_token.keys():
                d[key] = access_token[key]

            print("Successfully obtained Twitter API key for %s"%item_)

            return d




class FilesKeymaker(Keymaker):
    """
    Makes keys by iterating through a directory
    and making a key for each file.
    """
    def __init__(self, extension=''):
        Keymaker.__init__(self)
        self.files_extension = extension

    def make_keys(self,files_dir,keys_out_dir='keys/',interactive=True):
        """
        Make multiple keys.

        Go through each file and ask the user, 
        one by one, if they want to make a key for it.

        This bypasses the make_a_key() method
        defined in Sheep, and calls
        _make_a_key() directly.

        If interative=False, this simply passes through.
        """
        # Step 1:
        # Take care of file related-tasks for this bot
        # (finding files, storing files)

        # Get list of files from which we will create bots 
        if self.files_extension == '':
            files = glob.glob( join(files_dir, "*") )
        else:
            files = glob.glob( join(files_dir, "*.%s"%(self.files_extension) ) )

        if(len(files)==0):
            raise Exception("FilesKeymaker: Error: no files found!")

        files.sort()

        # Each bot needs to save its own file.
        # This sets the key that stores that info.
        self.file_key = 'file'


        # Step 2:
        # Iterate over each file and ask the user if 
        # they want to make a key for that file
        for f in files:

            full_file = join(files_dir,f)

            d = self._make_a_key(full_file, interactive=interactive)

            if(d != {}):

                d[self.file_key] = full_file

                # Step 2.5: Export our Sheep key info to a JSON file
                subprocess.call(["mkdir","-p",keys_out_dir])
                full_keys_file = re.sub(files_dir,keys_out_dir,full_file)
                _, ext = splitext(full_keys_file)

                if(self.files_extension == ''):
                    keys_file = full_keys_file+".json"
                else:
                    keys_file = re.sub(ext,'.json',full_keys_file)

                with open(keys_file, 'w') as outfile:
                      json.dump(d, outfile)
                print("Successfully exported a key bundle for file %s to JSON file %s"%(full_file, keys_file))

            else:
                # If we run non-interactively (test),
                # this is what we will get
                print("Did not export a key bundle for file %s (no auth step!)"%(full_file))


class TxtKeymaker(FilesKeymaker):
    """
    Makes keys by iterating hrough a directory 
    and making a key for each .txt file. 
    """
    def __init__(self):
        FilesKeymaker.__init__(self,extension='txt')


