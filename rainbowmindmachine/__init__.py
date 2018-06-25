from .TwitterShepherd import *
from .TwitterSheep import *
from .SocialSheep import *
from .PoemSheep import *
from .PhotoADaySheep import *
from .queneau import DialogueAssembler
from .QueneauSheep import *

import boringmindmachine as bmm
# alias
class TwitterKeymaker(bmm.TwitterKeymaker):
    """
    To change the way the GithubKeymaker works,
    make changes in boringmindmachine, which
    defines all Keymakers.
    """
    pass
class FilesKeymaker(bmm.FilesKeymaker):
    """
    See boringmindmachine
    """
    pass
class TxtKeymaker(bmm.TxtKeymaker):
    """
    See boringmindmachine
    """
    pass
