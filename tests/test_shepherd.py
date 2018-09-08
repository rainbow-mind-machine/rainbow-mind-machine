import rainbowmindmachine as rmm
from unittest import TestCase
import logging
import sys, os, subprocess, logging
import json
from .utils import captured_output, LoggingContext
import nose

from io import StringIO
from unittest.mock import patch

"""
Test Shepherd classes
"""


thisdir = os.path.abspath(os.path.dirname(__file__))

class TestShepherd(TestCase):
    """
    Test the Shepherd class.
    """
    keys_dir = "tests/shepherd_test_keys/"

    @classmethod
    def setUpClass(self):
        """
        Create fake bot keys to simulate
        the output of the Keymaker.
        We create a bare minimum fake key.
        """
        # These parameters go in a JSON file and are given to the Sheep on creation.
        # The name of the bot key JSON file is set by the 'json' item below.
        # 
        # Here, we create two fake bot keys for two bots
        # 
        fake_bot_keys = [{
            'consumer_token' : 'AAAAA1',
            'consumer_token_secret' : 'BBBBB1',
            'oauth_token' : 'CCCCC1',
            'oauth_token_secret' : 'DDDDD1',
            'user_id' : '00000000',
            'screen_name' : 'EEEEE1',
            'name' : 'FFFFF1',
            'json' : 'GGGGG1.json'
        },
        {
            'consumer_token' : 'AAAAA2',
            'consumer_token_secret' : 'BBBBB2',
            'oauth_token' : 'CCCCC2',
            'oauth_token_secret' : 'DDDDD2',
            'user_id' : '00000000',
            'screen_name' : 'EEEEE2',
            'name' : 'FFFFF2',
            'json' : 'GGGGG2.json'
        }]

        if not os.path.exists(self.keys_dir):
            os.mkdir(self.keys_dir)

        for bot_key in fake_bot_keys:
            ofile = os.path.join(self.keys_dir, bot_key['json'])
            with open(ofile,'w') as f:
                json.dump(bot_key,f)


    def test_shepherd(self):
        """
        Create a simple Shepherd.

        The Shepherd expects keys to exist already (that's the Keymaker's job).
        It will create one Sheep per key.

        The Shepherd constructor requires a label for the flock,
        a directory where JSON keys (one key per Sheep) are located, 
        and what class of Sheep to use when creating Sheep.

        The Shepherd constructor calls _setup_keys() and _setup_sheep().

        Function _setup_keys() expects each key (a dictionary)
        to contain a key-value pair for 'oauth_token'.
        This oauth token is what the Keymaker helps you generate.
        If your keys do not have all required fields, 
        this is the method that will stop you.
        See _key_is_valid() method in Shepherd.py.

        Function _setup_sheep() iterates over each key processed
        by _setup_keys() and makes one Sheep from each key.
        """
        #################################
        ##### https://stackoverflow.com/a/31281467
        #####
        #with patch('sys.stdout', new=StringIO()) as fakeOutput:
        #    print('hello world')
        #    self.assertEqual(fakeOutput.getvalue().strip(), 'hello world')

        #    # this "with" block ensures we capture stdout
        #    with captured_output() as (out, err):

        # Create the Shepherd (this starts the logger)
        s = rmm.TwitterShepherd(
            json_keys_dir = 'tests/shepherd_test_keys',
            sheep_class = rmm.TwitterSheep
        )

        self.assertLogs('Creating flock')
        self.assertLogs('Successfully created')


    def test_queneau_shepherd(self):
        log_file = 'tests/test_queneau_shepherd.log'
        sh = rmm.TwitterShepherd(json_keys_dir = self.keys_dir,
                          flock_name = 'My Fake Flock',
                          sheep_class = rmm.QueneauSheep,
                          log_file = log_file)

        # we are passing it fake key data
        # non-existent json will only raise an error
        # if we ask the Sheep to tweet live.
        # (........so where do we do that??)


    @classmethod
    def tearDownClass(self):
        """
        Clean up the fake bot keys
        """
        rm_keys_dir = ['rm','-fr',self.keys_dir]
        subprocess.call(rm_keys_dir)

        rmlog_cmd = ['rm', '-rf', 'rainbowmindmachine.log']
        subprocess.call(rmlog_cmd)


