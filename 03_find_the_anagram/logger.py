# -*- coding: utf-8 -*-

import logging


def configure_logger(filename=None, level=logging.INFO, logger_name=__name__):
    """Utility function to create logger object by demand

        Args:
            filename (str, optional): Name of the file to write log.
            level (logging.level): Level of the log verbosity. Default
            is INFO.
            module_name (str): logger name. Default is calling module name.

        Returns:
            logger object
   """
    filename = filename if filename else "{}.log".format(__name__)
    logging.basicConfig(filename=filename, level=logging.INFO,
                        format='''%(asctime)s %(levelname)-8s[%(filename)s:%(lineno)d] %(message)s''',
                        datefmt="%d-%m-%Y:%H:%M:%S")
    logger = logging.getLogger(logger_name)
    return logger
