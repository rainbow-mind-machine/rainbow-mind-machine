import rainbowmindmachine as rmm
import os
from nose.tools import *
from util import FYI

FYI()

f = rmm.Shepherd('../keymaker_test/keys')

# test sequential action 
f.perform_action('dummy')

# test parallel pool action
f.perform_pool_action('echo')



