import logging

"""
Lumberjack is the logger.

Advanced configuration with logging:

    https://docs.python.org/3/library/logging.config.html#logging-config-api

can package up logging configuration dictionaries
as .yaml files, in addition to json, etc.

But that's a little too fancy for our purposes.
"""

LOGO = r'''
 ____    ____  ____  ____   ____    ___   __    __ 
|    \  /    ||    ||    \ |    \  /   \ |  |__|  |
|  D  )|  o  | |  | |  _  ||  o  )|     ||  |  |  |
|    / |     | |  | |  |  ||     ||  O  ||  |  |  |
|    \ |  _  | |  | |  |  ||  O  ||     ||  `  '  |
|  .  \|  |  | |  | |  |  ||     ||     | \      / 
|__|\_||__|__||____||__|__||_____| \___/   \_/\_/  
                                                   
         ___ ___  ____  ____   ___                 
        |   |   ||    ||    \ |   \                
        | _   _ | |  | |  _  ||    \               
        |  \_/  | |  | |  |  ||  D  |              
        |   |   | |  | |  |  ||     |              
        |   |   | |  | |  |  ||     |              
        |___|___||____||__|__||_____|              
                                                   
 ___ ___   ____    __  __ __  ____  ____     ___   
|   |   | /    |  /  ]|  |  ||    ||    \   /  _]
| _   _ ||  o  | /  / |  |  | |  | |  _  | /  [_   
|  \_/  ||     |/  /  |  _  | |  | |  |  ||    _]
|   |   ||  _  /   \_ |  |  | |  | |  |  ||   [_
|   |   ||  |  \     ||  |  | |  | |  |  ||     |
|___|___||__|__|\____||__|__||____||__|__||_____|


                        Hello, darling,
                            I'm the lumberjack logger,
                                here to configure your logs.
'''

class Lumberjack(object):
    """
    The Lumberjack class just configures the logs
    and then it's all finished.
    """

    def __init__(self, 
                 flock_name = 'Anonymous Flock of Cowards',
                 log_file = 'rainbowmindmachine.log',
                 **kwargs):
        """
        Initialize the logging module to log 
        output from bots to a user-specified file.

        By default, this is rainbowmindmachine.log 
        located in the directory in which the bot 
        script is run.

        The user also specifies a name (for the log).
        """

        # These are pretty solid, so hard-code them
        format_str = " ".join(['%(asctime)s', "[" + flock_name + "]", '%(message)s'])
        date_str = '%m-%d-%Y %H:%M:%S'

        # Configure logging
        logging.basicConfig(level = logging.INFO,
                            datefmt = date_str)

        formatter = logging.Formatter(format_str)

        logger = logging.getLogger('rainbowmindmachine')

        #fh = logging.FileHandler(log_file)
        #fh.setLevel(logging.INFO)
        #logger.addHandler(fh)

        #ch = logging.StreamHandler()
        #ch.setLevel(logging.INFO)
        #logger.addHandler(ch)

        logger.info(LOGO)
        logger.info("-"*40)
        logger.info("Flock name: %s"%(flock_name))
        logger.info("Flock log file: %s"%(log_file))
        logger.info("-"*40)

