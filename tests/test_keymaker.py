import rainbowmindmachine as rmm
from unittest import TestCase
from .utils import captured_output
import os

thisdir = os.path.abspath(os.path.dirname(__file__))

class TestKeymaker(TestCase):

    def test_default_keymaker(self):
        keymaker = rmm.Keymaker()

    def test_txt_keymaker(self):
        keymaker = rmm.TxtKeymaker()

        apikeys = os.path.join(thisdir,'apikeys.json')
        keymaker.set_apikeys_file(apikeys)

        txtdir = os.path.join(thisdir,'txt/')
        with captured_output() as (out, err):
            keymaker.make_keys(txtdir,interactive=False)
        output = out.getvalue().strip()
        self.assertIn('Did not export a key bundle', output)

    def test_files_keymaker(self):
        keymaker = rmm.FilesKeymaker()

        apikeys = os.path.join(thisdir,'apikeys.json')
        keymaker.set_apikeys_file(apikeys)

        filesdir = os.path.join(thisdir,'files/')
        with captured_output() as (out, err):
            keymaker.make_keys(filesdir,interactive=False)
        output = out.getvalue().strip()
        self.assertIn('Did not export a key bundle', output)


#keymaker = rmm.Keymaker()
#keymaker.make_a_key({
#        'name':'charlesreid1',
#        'json':'keys/charlesreid1.json'
#    })

