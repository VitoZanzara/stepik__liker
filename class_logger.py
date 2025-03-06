import sys
import logging
from config import log_level


def get_logger(name: str, level: str=log_level) -> logging.Logger:
    levels = {'DEBUG': logging.DEBUG, 'INFO': logging.INFO, 'WARNING': logging.WARNING,
              'ERROR': logging.ERROR, 'CRITICAL': logging.CRITICAL}
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    log_format = f"%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    log_format = f"%(asctime)s - [%(levelname)s] - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    logger = logging.getLogger(name)
    logger.setLevel(levels.get(level.upper(), logging.WARNING))
    logger_handler = logging.StreamHandler(sys.stdout)
    logger_formatter = logging.Formatter(log_format, datefmt='%H:%M:%S')
    logger_handler.setFormatter(logger_formatter)
    logger.addHandler(logger_handler)
    return logger


if __name__ == '__main__':
    logger = get_logger('test', level='DEBUG')
    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warning message')
    print(type(logger))