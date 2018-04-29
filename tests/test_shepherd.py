import rainbowmindmachine as rmm
from unittest import TestCase
import os
from .utils import captured_output

class TestShepherd(TestCase):

    @classmethod
    def setUpClass(self):
        # here we should create some fake keys
        pass

    def test_shepherd(self):
        # This should create a flock named 
        # "Anonymous Flock of Cowards"
        with captured_output() as (out, err):
            s = rmm.Shepherd(
                flock_name='test flock',
                json_key_dir='tests/keys',
                sheep_class=rmm.Sheep
            )
        output = out.getvalue().strip()
        self.assertIn('Creating flock', output)

    def test_queneau_shepherd(self):
        #log_file = 'tests/test_queneau_shepherd.log'
        #sh = rmm.Shepherd('keys/',
        #                  flock_name = 'My Apollo Flock',
        #                  sheep_class = rmm.QueneauSheep,
        #                  log_file = log_file)
        pass

