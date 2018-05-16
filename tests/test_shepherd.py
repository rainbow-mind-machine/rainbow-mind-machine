import rainbowmindmachine as rmm
from unittest import TestCase
import sys, os, subprocess, logging
from .utils import captured_output, LoggingContext


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
            'consumer_token' : 'AAAAA',
            'consumer_token_secret' : 'BBBBB',
            'oauth_token' : 'CCCCC',
            'oauth_token_secret' : 'DDDDD',
            'user_id' : '00000000',
            'screen_name' : 'EEEEE',
            'name' : 'FFFFF',
            'json' : 'GGGGG.json'
        },
        {
            'consumer_token' : 'AAAAA',
            'consumer_token_secret' : 'BBBBB',
            'oauth_token' : 'CCCCC',
            'oauth_token_secret' : 'DDDDD',
            'user_id' : '00000000',
            'screen_name' : 'EEEEE',
            'name' : 'FFFFF',
            'json' : 'GGGGG.json'
        }]

        mkdir_cmd = ['mkdir', '-p', self.keys_dir]
        subprocess.call(mkdir_cmd)


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
        logger = logging.getLogger('rainbowmindmachine')
        h = logging.StreamHandler(sys.stdout)

        # this "with" block ensures logs print to stdout
        with LoggingContext(logger, level=logging.INFO, handler=h, close=True):

            # this "with" block ensures we capture stdout
            with captured_output() as (out, err):

                # Create the Shepherd (this starts the logger)
                s = rmm.Shepherd(
                    flock_name = 'test flock',
                    json_keys_dir = 'tests/shepherd_test_keys',
                    sheep_class = rmm.Sheep
                )

            stderrlog = err.getvalue().strip()
            self.assertIn('Creating flock', stderrlog)
            self.assertIn('Successfully created', stderrlog)
            self.assertEqual('test flock',s.name)


    def test_queneau_shepherd(self):
        log_file = 'tests/test_queneau_shepherd.log'
        sh = rmm.Shepherd(json_keys_dir = 'keys/',
                          flock_name = 'My Apollo Flock',
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
        rmdir_cmd = ['rm', '-rf', self.keys_dir]
        subprocess.call(rmdir_cmd)

        rmlog_cmd = ['rm', '-rf', 'rainbowmindmachine.log']
        subprocess.call(rmlog_cmd)


