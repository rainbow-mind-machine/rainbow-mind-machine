import rainbowmindmachine as rmm
from unittest import TestCase
import sys, os, subprocess, logging
from .utils import captured_output, LoggingContext

class TestShepherd(TestCase):
    """
    Test the Shepherd class.

    This should be run after the Sheep
    and Keymaker tests.
    """

    @classmethod
    def setUpClass(self):
        """
        Create fake bot keys to simulate
        the output of the Keymaker.

        Fake bot keys have a couple of necessary
        key-value pairs, and some optional ones.

        Here we just create the bare minimum key.
        """
        key_dir = "tests/shepherd_test_keys/"
        # Note that this key should go in a JSON file,
        # since that's how the sheep takes its parameters.
        # Also, the name in json should be the name 
        # given to this key file (path must be specified separately)
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


    def test_shepherd(self):
        """
        Create a simple Shepherd.

        The Shepherd expects keys to exist already. 
        Constructor calls setup_keys and setup_sheep.
        Function setup_keys expects each key to have 'oauth_token'.
        Function setup_sheep expects a list of JSON files
        """
        logger = logging.getLogger('rainbowmindmachine')
        h = logging.StreamHandler(sys.stdout)

        # this "with" block ensures logs print to stdout
        with LoggingContext(logger, level=logging.INFO, handler=h, close=True):

            # this "with" block ensures we capture stdout
            with captured_output() as (out, err):

                # Create the Shepherd (this starts the logger)
                s = rmm.Shepherd(
                    flock_name='test flock',
                    json_key_dir='tests/keys',
                    sheep_class=rmm.Sheep
                )

            stderrlog = err.getvalue().strip()
            self.assertIn('Creating flock', stderrlog)
            self.assertIn('Successfully created', stderrlog)
            self.assertEqual('test flock',s.name)


    def test_queneau_shepherd(self):
        #log_file = 'tests/test_queneau_shepherd.log'
        #sh = rmm.Shepherd('keys/',
        #                  flock_name = 'My Apollo Flock',
        #                  sheep_class = rmm.QueneauSheep,
        #                  log_file = log_file)
        pass

