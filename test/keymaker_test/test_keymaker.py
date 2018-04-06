import rainbowmindmachine as rmm
import os
import subprocess
from nose.tools import *
from .util import FYI

FYI()

subprocess.call(["mkdir","-p","keys"])

keymaker = rmm.Keymaker()
keymaker.make_a_key({
        'name':'charlesreid1',
        'json':'keys/charlesreid1.json'
    })

