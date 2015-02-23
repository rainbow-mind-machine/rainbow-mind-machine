import rainbowmindmachine as rmm
import os
from nose.tools import *
from apikeys import *

keymaker = rmm.TxtKeymaker()
keymaker.make_keys('txt/')

