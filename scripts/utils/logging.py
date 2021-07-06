from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from scripts.utils.config import LOG_LEVEL, LOG_HANDLER_NAME, BASE_LOG_PATH
from scripts.utils.config import LOG_HANDLER_BACKUP_COUNT, LOG_HANDLER_WHEN, LOG_HANDLER_INTERVAL
import logging
from logging.handlers import TimedRotatingFileHandler
import os



EXTRA = {}

formatter = '%(asctime)s %(levelname)5s %(name)s %(message)s'

def get_logger(logger_fn=None,log_handler_name=LOG_HANDLER_NAME,worker=None, extra=None,formatter=formatter):
    """
    Purpose : To create logger .
    :param log_handler_name: Name of the log handler.
    :param extra: extra args for the logger
    :return: logger object.
    """
    if extra is None:
        extra = EXTRA

    if worker:
        log_handler_name =log_handler_name+"_"+worker


    if logger_fn is None:
        logger = logging.getLogger(log_handler_name)
        logger.setLevel(LOG_LEVEL.strip().upper())
    else:
        logger = logger_fn(log_handler_name)
        logger.propagate = False
    log_path = os.path.join(BASE_LOG_PATH, log_handler_name + ".log")
    log_handler = logging.StreamHandler()
    log_handler.setLevel(LOG_LEVEL)
    formatter = logging.Formatter(formatter)
    log_handler.setFormatter(formatter)
    handler = TimedRotatingFileHandler(log_path, when=LOG_HANDLER_WHEN, interval=LOG_HANDLER_INTERVAL,
                                       backupCount=LOG_HANDLER_BACKUP_COUNT)
    handler.setFormatter(formatter)
    logger.addHandler(log_handler)
    logger.addHandler(handler)

    logger = logging.LoggerAdapter(logger, extra)

    return logger



logger = get_logger()