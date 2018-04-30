import rainbowmindmachine as rmm
from unittest import TestCase
import os


"""
Test Sheep classes
"""


thisdir = os.path.abspath(os.path.dirname(__file__))

class TestSheep(TestCase):
    """
    Test the Sheep class.

    This should be done before testing the Shepherd, 
    to limit what can go wrong.
    """

    @classmethod
    def setUpClass(self):
        """
        This is basically replicating Shepherd.setup_sheep()
        
        Shepherd.setup_sheep() algorithm:
        - loop over each json file
        - for each json file,
        - create a bot
        - assign json file to bot

        The Keymaker makes the bot keys.

        The Shepherd spot-checks the bot keys.

        The Sheep loads the bot keys.
        """
        pass

