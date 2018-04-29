import rainbowmindmachine as rmm
from unittest import TestCase
import os

class TestShepherd(TestCase):

    @classmethod
    def setUpClass(self):
        # here we should create some fake keys
        pass

    def test_shepherd(self):
        s = rmm.Shepherd({
            'json_key_dir': 'tests/keys',
            'sheep_class': rmm.Sheep
        })

