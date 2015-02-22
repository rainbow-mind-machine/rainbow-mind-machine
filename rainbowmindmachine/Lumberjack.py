from __init__ import LOG_FILE
import logging

"""
Lumberjack is the logger.
Get it?
"""

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(message)s',
                    datefmt='%m-%d-%Y %H:%M',
                    filename=LOG_FILE,
                    filemode='w')
 
logging.info('Hello darling! I am the Lumberjack logger.')

