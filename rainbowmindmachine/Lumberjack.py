import logging

"""
Lumberjack is the logger.
Get it?
"""

log_file = 'test_log.out'
 
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename=log_file,
                    filemode='w')
 
logging.info('Hello file!')

