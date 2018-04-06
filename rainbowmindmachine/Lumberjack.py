import logging

"""
Lumberjack is the logger.

advanced configuration with logging:

    https://docs.python.org/3/library/logging.config.html#logging-config-api

can package up configuration dictionaries
as .yaml files, in addition to json, etc.

A little too fancy for our purposes.
"""

class Lumberjack (object):

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
        format_str = " ".join(['%(asctime)s', bot_name, '%(message)s'])
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
        logging.getLogger('').addHandler(console)

        logo = r'''
  _                 _               _            _
 | |               | |             (_)          | |
 | |_   _ _ __ ___ | |__   ___ _ __ _  __ _  ___| | __
 | | | | | '_ ` _ \| '_ \ / _ \ '__| |/ _` |/ __| |/ /
 | | |_| | | | | | | |_) |  __/ |  | | (_| | (__|   <
 |_|\__,_|_| |_| |_|_.__/ \___|_|  | |\__,_|\___|_|\_\
                                  _/ |
                                 |__/

                        Hello, darling.
                            I'm the lumberjack logger.
'''
        logging.info(logo)


    def log(self, msg):
        logging.info(msg)

