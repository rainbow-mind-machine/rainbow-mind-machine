import rainbowmindmachine as rmm
from unittest import TestCase
import logging
import os, subprocess
from .utils import captured_output


"""
Test Keymaker classes
"""


console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
logging.getLogger('').addHandler(console)


thisdir = os.path.abspath(os.path.dirname(__file__))

class TestKeymaker(TestCase):
    """
    Test the Keymaker class.

    This focuses on testing the constructors
    and the API key initialization process.
    """
    @classmethod
    def setUpClass(self):
        self.keys_dir = os.path.join( thisdir, "test_keymaker_keys" )
        self.api_keys = os.path.join( thisdir, "apikeys.json" )

        # Note: this gives the same outcome as 
        # hard-coding the path "tests"


    def test_default_keymaker_apikeys_env(self):
        """
        Test ability to create single key using consumer token from environment vars
        """
        keymaker = rmm.TwitterKeymaker()

        # Set application API keys
        os.environ['CONSUMER_TOKEN'] = 'AAAAA'
        os.environ['CONSUMER_TOKEN_SECRET'] = 'BBBBB'
        keymaker.set_apikeys_env()

        # Create bot API keys
        with captured_output() as (out, err):
            keymaker.make_a_key(
                name = 'test_default_keymaker_apikeys_env',
                json_target = 'test_default_keymaker_apikeys_env.json',
                keys_out_dir = self.keys_dir,
                interactive = False
            )

        # Clean up
        os.environ['CONSUMER_TOKEN'] = ''
        os.environ['CONSUMER_TOKEN_SECRET'] = ''

        # Assert
        output = out.getvalue().strip()
        self.assertIn('Creating fake Twitter key', output)


    def test_default_keymaker_apikeys_file(self):
        """
        Test ability to create single key using consumer token/secret from JSON file
        """
        keymaker = rmm.TwitterKeymaker()

        # Set application API keys
        apikeys = os.path.join(thisdir,'apikeys.json')
        keymaker.set_apikeys_file(apikeys)

        # Create bot API keys
        with captured_output() as (out, err):
            keymaker.make_a_key(
                name = 'test_default_keymaker_apikeys_file',
                json_target = 'test_default_keymaker_apikeys_file.json',
                keys_out_dir=self.keys_dir,
                interactive=False
            )

        # Assert
        output = out.getvalue().strip()
        self.assertIn('Creating fake Twitter key', output)


    def test_default_keymaker_apikeys_dict(self):
        """
        Test ability to create single key using consumer token/secret from dictionary
        """
        keymaker = rmm.TwitterKeymaker()

        # Set application API keys
        keymaker.set_apikeys_dict({ 
            'consumer_token': 'AAAAA',
            'consumer_token_secret': 'BBBBB'
        })

        # Create bot API keys
        with captured_output() as (out, err):
            keymaker.make_a_key(
                name = 'test_default_keymaker_apikeys_dict',
                json_target = 'test_default_keymaker_apikeys_dict.json',
                keys_out_dir = self.keys_dir,
                interactive = False
            )

        # Assert
        output = out.getvalue().strip()
        self.assertIn('Creating fake Twitter key', output)


    @classmethod
    def tearDownClass(self):
        # Remove the keys directory we created
        subprocess.call(['rm','-rf',self.keys_dir])



class TestFilesKeymaker(TestCase):
    """
    Test file-based keymaker classes.
    """

    @classmethod
    def setUpClass(self):
        self.keys_dir = os.path.join( thisdir, "test_keymaker_files_keys" )
        self.api_keys = os.path.join( thisdir, "apikeys.json" )


    def test_files_keymaker(self):
        """
        Test the FilesKeymaker, which makes one key
        for each file with a given extension 
        in a given directory.
        """
        keymaker = rmm.FilesKeymaker()

        # Set application API keys
        apikeys = os.path.join(thisdir,'apikeys.json')
        keymaker.set_apikeys_file(apikeys)

        # Create bot API keys
        # from files in filesdir
        filesdir = os.path.join(thisdir,'files/')
        with captured_output() as (out, err):
            keymaker.make_keys( 
                    filesdir,
                    keys_out_dir = self.keys_dir,
                    interactive = False
            )

        # Assert
        output = out.getvalue().strip()
        self.assertIn('Creating fake Twitter key', output)


    def test_txt_keymaker(self):
        """
        Test the TxtKeymaker, which makes one key
        for each .txt file in a given directory.
        """
        keymaker = rmm.TxtKeymaker()

        # Set application API keys
        apikeys = os.path.join(thisdir,'apikeys.json')
        keymaker.set_apikeys_file(apikeys)

        # Create bot API keys
        txtdir = os.path.join(thisdir,'txt/')
        with captured_output() as (out, err):
            keymaker.make_keys(
                    txtdir,
                    keys_out_dir = self.keys_dir,
                    interactive = False
            )

        # Assert
        output = out.getvalue().strip()
        self.assertIn('Creating fake Twitter key', output)


    @classmethod
    def tearDownClass(self):
        # Remove the keys directory we created
        subprocess.call(['rm','-rf',self.keys_dir])

