import rainbowmindmachine as rmm
from unittest import TestCase
import os
from .utils import captured_output

thisdir = os.path.abspath(os.path.dirname(__file__))

class TestKeymaker(TestCase):

    @classmethod
    def setUpClass(self):
        self.keys_dir = 'tests/keys'

    def test_default_keymaker_apikeys_env(self):
        """
        Test ability to create single key using consumer token from environment vars
        """
        os.environ['CONSUMER_TOKEN'] = 'AAAAA'
        os.environ['CONSUMER_TOKEN_SECRET'] = 'BBBBB'

        keymaker = rmm.Keymaker()
        keymaker.set_apikeys_env()

        with captured_output() as (out, err):
            keymaker.make_a_key({
                'name' : 'test_default_keymaker_apikeys_env',
                'json' : 'test_default_keymaker_apikeys_env.json'
            },
            keys_out_dir=self.keys_dir,
            interactive=False)

        os.environ['CONSUMER_TOKEN'] = ''
        os.environ['CONSUMER_TOKEN_SECRET'] = ''

        output = out.getvalue().strip()

    def test_default_keymaker_apikeys_file(self):
        """
        Test ability to create single key using consumer token/secret from JSON file
        """
        keymaker = rmm.Keymaker()

        apikeys = os.path.join(thisdir,'apikeys.json')
        keymaker.set_apikeys_file(apikeys)

        with captured_output() as (out, err):
            keymaker.make_a_key({
                'name' : 'test_default_keymaker_apikeys_file',
                'json' : 'test_default_keymaker_apikeys_file.json'
            },
            keys_out_dir=self.keys_dir,
            interactive=False)

        output = out.getvalue().strip()
        self.assertIn('Did not export a key bundle', output)

    def test_default_keymaker_apikeys_dict(self):
        """
        Test ability to create single key using consumer token/secret from dictionary
        """
        keymaker = rmm.Keymaker()

        keymaker.set_apikeys_dict({ 
            'consumer_token': 'AAAAA',
            'consumer_token_secret': 'BBBBB'
        })

        with captured_output() as (out, err):
            keymaker.make_a_key({
                'name' : 'test_default_keymaker_apikeys_dict',
                'json' : 'test_default_keymaker_apikeys_dict.json'
            },
            keys_out_dir=self.keys_dir,
            interactive=False)

        output = out.getvalue().strip()
        self.assertIn('Did not export a key bundle', output)

    def test_files_keymaker(self):
        """
        Test the FilesKeymaker, which makes one key
        for each file with a given extension 
        in a given directory.
        """
        keymaker = rmm.FilesKeymaker()

        apikeys = os.path.join(thisdir,'apikeys.json')
        keymaker.set_apikeys_file(apikeys)

        filesdir = os.path.join(thisdir,'files/')
        with captured_output() as (out, err):
            keymaker.make_keys(filesdir,
                keys_out_dir=self.keys_dir,
                interactive=False)
        output = out.getvalue().strip()
        self.assertIn('Did not export a key bundle', output)

    def test_txt_keymaker(self):
        """
        Test the TxtKeymaker, which makes one key
        for each .txt file in a given directory.
        """
        keymaker = rmm.TxtKeymaker()

        apikeys = os.path.join(thisdir,'apikeys.json')
        keymaker.set_apikeys_file(apikeys)

        txtdir = os.path.join(thisdir,'txt/')
        with captured_output() as (out, err):
            keymaker.make_keys(txtdir,
                keys_out_dir=self.keys_dir,
                interactive=False)
        output = out.getvalue().strip()
        self.assertIn('Did not export a key bundle', output)

    @classmethod
    def tearDownClass(self):
        # Remove the keys directory we created
        subprocess.call(['rm','-rf',self.keys_dir])

