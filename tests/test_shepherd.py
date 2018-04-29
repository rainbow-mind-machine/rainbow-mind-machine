import rainbowmindmachine as rmm
from unittest import TestCase
import sys, os, subprocess, logging
from .utils import captured_output, LoggingContext

class TestShepherd(TestCase):

    @classmethod
    def setUpClass(self):
        # here we should create some fake keys
        pass

    def test_shepherd(self):
        # This should create a flock named 
        # "Anonymous Flock of Cowards"
        logger = logging.getLogger('rainbowmindmachine')
        h = logging.StreamHandler(sys.stdout)

        # this with block ensures logs print to stdout
        with LoggingContext(logger, level=logging.INFO, handler=h, close=True):

            # this with block ensures we capture stdout
            with captured_output() as (out, err):

                # Create the Shepherd (this starts the logger)
                s = rmm.Shepherd(
                    flock_name='test flock',
                    json_key_dir='tests/keys',
                    sheep_class=rmm.Sheep
                )

            stderrlog = err.getvalue().strip()
            self.assertIn('Creating flock', stderrlog)

    def test_queneau_shepherd(self):
        #log_file = 'tests/test_queneau_shepherd.log'
        #sh = rmm.Shepherd('keys/',
        #                  flock_name = 'My Apollo Flock',
        #                  sheep_class = rmm.QueneauSheep,
        #                  log_file = log_file)
        pass

