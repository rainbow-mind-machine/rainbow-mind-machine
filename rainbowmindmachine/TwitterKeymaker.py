import boringmindmachine as bmm

import logging
import subprocess
import os, re, glob
import json
from os.path import isfile, isdir, exists
from os.path import join, basename, splitext
import urllib
import oauth2 as oauth


class TwitterKeymaker(bmm.BoringOAuthKeymaker):
    """
    We do only what we are meant to do.

    TwitterKeymaker takes a set of items and asks the user
    if they would like to create a key from each item.

    TwitterKeymaker handles the OAuth mechanism and does the 
    three-legged authentication dance with Twitter.

    This results in one public/private key pair per sheep.
    With a sheep's keys, you can tweet as that sheep.
    """
    def __init__(self):
        super().__init__('consumer_token','consumer_token_secret')


    # ---
    # Single Key Method:
    # The workhorse.

    def make_a_key( self,
                    name,
                    json_target,
                    keys_out_dir='keys/',
                    **kwargs):
        """
        Public method to make a single key from a single item.

            name :          Label for the bot

            json_target :   The name of the JSON file in which to save
                            the bot OAuth key (all paths are ignored).

            keys_out_dir :  Directory in which to place final JSON keys
                            containing OAuth tokens and other bot info

            interactive :   If set to False, this turns off interactivity
                            (this option is used for tests)

        All kwargs are passed into the key file.

        Also note: this is the only interactive method in the library,
        so we print to stdout instead of using logging.
        """
        if os.path.isdir(keys_out_dir) is False:
            subprocess.call(['mkdir','-p',keys_out_dir])

        if 'interactive' in kwargs and kwargs['interactive'] is False:
            pass
        else:
            kwargs['interactive'] = True

        # strip paths from json_target file name
        json_target = os.path.basename(json_target)

        # ------------8<----------------8<--------------
        # Begin Twitter-Specific Section

        # the output of this function are
        # json key files. if no key file
        # will be made, just return.

        if(not self.apikeys_set):
            err = "TwitterKeymaker Error: make_a_key(): API keys were not set for the Shepherd."
            logging.error(err)
            raise Exception(err)

        msgs = ["="*40, "Bot Name: %s"%(name), "="*40]
        msg = "\n".join(msgs)
        logging.info(msg)
        #print(msg)

        # Step 1: get item (done)

        # Step 2: make Twitter API key for each item

        # (Handle non-interactive test case first)
        if not kwargs['interactive']:
            msg = "TwitterKeymaker: make_a_key(): Creating fake Twitter key"
            logging.info(msg)
            print(msg)
            d = dict(consumer_token="AAAAA",
                     consumer_token_secret="BBBBB",
                     oauth_token = "CCCCC",
                     oauth_token_secret = "DDDDD",
                     user_id = "00000",
                     screen_name = "EEEEE"
            )
            keys_out = join(keys_out_dir,json_target)
            with open(keys_out,'w') as outfile:
                json.dump(d,outfile)
            return

        make_key = ''
        while make_key != 'y' and make_key != 'n':
            make_key = input('Make key? (y/n) ')

        if make_key=='n':
            msg = "Skipping keymaking for %s"%name
            logging.info(msg)
            print(msg)
            return

        msg = "TwitterKeymaker: make_a_key(): Starting keymaking for %s"%name
        logging.info(msg)
        print(msg)

        consumer = oauth.Consumer(self.credentials[self.token],
                                  self.credentials[self.secret])
        client = oauth.Client(consumer)

        request_token_url = 'https://api.twitter.com/oauth/request_token'
        authorize_url = 'https://api.twitter.com/oauth/authorize'
        access_token_url = 'https://api.twitter.com/oauth/access_token'

        # Step 2.1: Get a request token. 
        # App uses this to give user a login link.
        # https://dev.twitter.com/docs/api/1/get/oauth/authenticate
        resp, content = client.request(request_token_url,"GET")
        if resp['status'] != '200':
            msg = "Invalid response %s. If apikeys.py is present, your keys may be invalid." % resp['status']
            logging.error(msg)
            raise Exception(msg)

        request_token = dict(urllib.parse.parse_qsl(content))
        oauth_token = request_token[b'oauth_token'].decode('utf-8')
        oauth_token_secret = request_token[b'oauth_token_secret'].decode('utf-8')

        print("Request token received.")
        print("Visit the following app authorization link:")
        print("%s?oauth_token=%s" % (authorize_url, oauth_token ))
        print("")
        print("Sign in as the user to be associated with %s"%name)
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
            return

        elif oauth_verifier == 'r':

            # go through the oauth dance again
            self.make_a_key(name,
                            json_target,
                            keys_out_dir,
                            **kwargs)
        
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

            resp, content = client.request(access_token_url, "POST")
            access_token = dict(urllib.parse.parse_qsl(content))

            def strip(mystr):
                if(type(mystr)==type(b'aaaaaaaa')):
                    return mystr.decode('utf-8')
                return mystr

            # Step 2.4: Make a dict with all 
            # final key info and Sheep info
            # (twitter - y u use binary strings??)

            d = {}

            for key in self.credentials.keys():
                value = self.credentials[key]
                d[strip(key)] = strip(value)

            for key in access_token.keys():
                value = access_token[key]
                d[strip(key)] = strip(value)

            for key in kwargs.keys():
                d[key] = kwargs[key]


            msg = "TwitterKeymaker: make_a_key(): Successfully obtained Twitter API key for Sheep %s"%(name)
            logging.info(msg)
            print(msg)

            print("-------------------------------")


            # Step 2.5: Round this out by making the key files
            # Make a key dir
            subprocess.call(["mkdir","-p",keys_out_dir])

            keys_out = join(keys_out_dir,json_target)

            with open(keys_out,'w') as outfile:
                json.dump(d,outfile)

            msg = "Twitter Keymaker: make_a_key(): Successfully exported a key bundle for item %s to JSON file %s"%(name,keys_out)
            logging.info(msg)
            print(msg)



class FilesKeymaker(TwitterKeymaker):
    """
    Makes keys by iterating through a directory
    and making a key for each file.
    """
    def __init__(self, extension=''):
        TwitterKeymaker.__init__(self)
        self.files_extension = extension

    def make_keys(self,
                  files_dir,
                  keys_out_dir='keys/',
                  **kwargs):
        """
        Make multiple keys.

        Go through each file and ask the user, 
        one by one, if they want to make a key for it.

        This calls the make_a_key() method in the Keymaker class.
            
        This passes kwargs straight through to make_a_key()
        so all options for TwitterKeymaker.make_a_key() are 
        same for FilesKeymaker.make_keys()
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
            msg = "FilesKeymaker Error: make_keys(): no files found! Looked in %s"%(files_dir)
            logging.error(msg)
            raise Exception(msg)

        files.sort()

        # Each bot needs to stash the name of the file it is assigned.
        # That's what this variable is.
        self.file_key = 'file'

        # Step 2:
        # Iterate over each file and make a key from each.
        # This is a list of filenames with relative paths
        # (that means it includes files_dir)
        for full_file in files:

            msg = "FilesKeymaker: make_keys(): Creating a key from file %s"%(full_file)
            logging.debug(msg)

            # To get the key file that corresponds to this (random) file, 
            # we swap out the files directory name with the keys directory name,
            # then copy the file name but use a .json extension instead

            full_keys_file = re.sub(files_dir,keys_out_dir,full_file)

            base, ext = splitext(basename(full_keys_file))
            if(self.files_extension == ''):
                full_keys_file = full_keys_file+".json"
            else:
                full_keys_file = re.sub(ext,'.json',full_keys_file)

            self.make_a_key(name = base,
                            json_target = full_keys_file,
                            keys_out_dir = keys_out_dir,
                            file = full_file,
                            **kwargs)



class TxtKeymaker(FilesKeymaker):
    """
    Makes keys by iterating through a directory 
    and making a key for each .txt file. 
    """
    def __init__(self):
        FilesKeymaker.__init__(self,extension='txt')


