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

    def __init__(self, 
                 flock_name = 'Anonymous Flock of Cowards',
                 log_level = logging.INFO, 
                 log_file = 'rainbowmindmachine.log'):
        """
        Initialize the logging module to log 
        output from bots to a user-specified file.

        By default, this is rainbowmindmachine.log 
        located in the directory in which the bot 
        script is run.

        The user also specifies a name (for the log),
        and a log level. (Currently, everything is INFO.)
        """

        # These are pretty solid, so hard-code them
        format_str = " ".join(['%(asctime)s', "[" + flock_name + "]", '%(message)s'])
        date_str = '%m-%d-%Y %H:%M:%S'

        # Configure logging
        logging.basicConfig(level = log_level,
                            format = format_str,
                            datefmt = date_str,
                            filename = log_file,
                            filemode = 'w')

        # Set log target: console
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        self.logger = logging.getLogger('rainbowmindmachine')
        self.logger.addHandler(console)

        logo = LOGO
        self.logger.info(logo)
        self.logger.info("-"*40)
        self.logger.info("Flock name: %s"%(flock_name))
        self.logger.info("Flock log file: %s"%(log_file))
        self.logger.info("-"*40)

