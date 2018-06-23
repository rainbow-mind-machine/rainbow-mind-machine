from .RainbowLumberjack import *
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
    pass
class FilesKeymaker(bmm.FilesKeymaker):
    pass
class TxtKeymaker(bmm.TxtKeymaker):
    pass
