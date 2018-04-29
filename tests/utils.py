import sys
from contextlib import contextmanager
from io import StringIO
import logging

@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err



# https://docs.python.org/3/howto/logging-cookbook.html

class LoggingContext(object):
    def __init__(self, logger, level=None, handler=None, close=True):
        self.logger = logger
        self.level = level
        self.handler = handler
        self.close = close

    def __enter__(self):
        if self.level is not None:
            self.old_level = self.logger.level
            self.logger.setLevel(self.level)
        if self.handler:
            self.logger.addHandler(self.handler)

    def __exit__(self, et, ev, tb):
        if self.level is not None:
            self.logger.setLevel(self.old_level)
        if self.handler:
            self.logger.removeHandler(self.handler)
        if self.handler and self.close:
            self.handler.close()
        # implicit return of None => don't swallow exceptions


# # Example using the logging context handler:
# 
# if __name__ == '__main__':
#     logger = logging.getLogger('foo')
#     logger.addHandler(logging.StreamHandler())
#     logger.setLevel(logging.INFO)
#     logger.info('1. This should appear just once on stderr.')
#     logger.debug('2. This should not appear.')
#     with LoggingContext(logger, level=logging.DEBUG):
#         logger.debug('3. This should appear once on stderr.')
#     logger.debug('4. This should not appear.')
#     h = logging.StreamHandler(sys.stdout)
#     with LoggingContext(logger, level=logging.DEBUG, handler=h, close=True):
#         logger.debug('5. This should appear twice - once on stderr and once on stdout.')
#     logger.info('6. This should appear just once on stderr.')
#     logger.debug('7. This should not appear.')

