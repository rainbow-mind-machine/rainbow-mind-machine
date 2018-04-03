LOG_FILE = "/tmp/rainbowmindmachine.log"
from Lumberjack import *
from Keymaker import *
from Shepherd import *
from Sheep import *
from PoemBotFlock import *
from PhotoBotFlock import *
try:
    from queneau import DialogueAssembler
    from QueneauBotFlock import *
except ImportError:
    pass

