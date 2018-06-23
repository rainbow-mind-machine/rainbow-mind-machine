import boringmindmachine as bmm
import logging

"""
Lumberjack is the logger.
"""

class RainbowLumberjack(bmm.BoringLumberjack):
    """
    The Lumberjack class just configures the logs
    and then it's all finished.

    Honestly, we'll almost never need to extend this.
    """

    LOGO = r'''

         )RA( )IN( )BO( )WM( )IN( )DM( )AC( )HI( )NE(


                  Don't mind me -
                    I'm the Lumberjack, 
                        configuring your logs.

'''

    def __init__(self, 
                 flock_name,
                 log_file = 'rainbowmindmachine.log',
                 **kwargs):
        """
        Call the super constructor to set up a mind machine log.
        Then set up a rainbow mind machine log.
        """
        super().__init__(
                flock_name,
                log_file = log_file,
                **kwags
        )

        logger = logging.getLogger('rainbowmindmachine')

        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.INFO)
        logger.addHandler(fh)

        logger.info(self.LOGO)
        logger.info("-"*40)
        logger.info("Flock name: %s"%(flock_name))
        logger.info("Flock log file: %s"%(log_file))
        logger.info("-"*40)


