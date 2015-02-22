import rainbowmindmachine as rmm
import os
from nose.tools import *

keymaker = rmm.Keymaker()
keymaker.manually_make_key({
        'name':'charlesreid1',
        'json':'charlesreid1.json'
    })

"""
class BaseTest(object):
    def __init__(self):
        pass
    def run_test(self):
        try:
            assert True
        except AssertionError:
            err = "Error!"
            raise Exception(err)
"""
