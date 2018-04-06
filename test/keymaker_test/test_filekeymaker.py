import rainbowmindmachine as rmm
import os
from nose.tools import *
from .util import FYI

FYI()

keymaker = rmm.FilesKeymaker()
keymaker.make_keys('files/')

