# System Imports.
import os
import logging.config

# User imports
from resources import const_vars


def get_logger(caller):
    """
    Returns an instance of the logger. Always pass the __name__ attribute.
    By calling through here, guarantees that logger will always have proper settings loaded.
    :param caller: __name__ attribute of caller.
    :return: Instance of logger, associated with caller's __name__.
    """
    return logging.getLogger(caller)


def cond_logger(logger, type, message, create_log, exc_info=False):
    """
    A conditional logger for when logging is not always called.
    Ex: There's no reason to log precautionary measures that are okay to fail silently.
    Creating a method helps prevent many small if statements from cluttering code.
    :param logger: Instance of logger to use.
    :param type: Logging type. IE, debug, info, etc.
    :param message: Message to log.
    :param create_log: Boolean dictating if this instance of log is printed.
    """
    if create_log:
        getattr(logger,type)(str(message), exc_info=exc_info)


# Find user directory and logging path.
# user_root_dir = '/home/pi/'
# log_dir = os.path.join(user_root_dir, 'Documents/PiCamPython/logs')
log_dir = const_vars.LOG_DIR
if not os.path.exists(log_dir):
    print('Creating logging folders.')
    os.makedirs(log_dir)


# Dictionary style logging options.
LOGGING = {
    'version': 1,
    'formatters': {
        # Simple logging. Includes message type and actual message.
        'simple': {
            'format': '[%(levelname)s] [%(filename)s %(lineno)d]: %(message)s',
        },
        # Basic logging. Includes date, message type, file originated, and actual message.
        'standard': {
            'format': '%(asctime)s [%(levelname)s] [%(filename)s %(lineno)d]: %(message)s',
        },
        # Verbose logging. Includes standard plus the process number and thread id.
        'verbose': {
            'format': '%(asctime)s [%(levelname)s] [%(filename)s %(lineno)d] || %(process)d %(thread)d || %(message)s',
        },
    },
    'handlers': {
        # Sends log message to the void. May be useful for debugging.
        'null': {
            'class': 'logging.NullHandler',
        },
        # To console.
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        # Debug Level to file.
        'file_debug': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(log_dir, 'debug.log'),
            'maxBytes': 1024*1024*10,
            'backupCount': 10,
            'formatter': 'standard',
        },
        # Info Level to file.
        'file_info': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(log_dir, 'info.log'),
            'maxBytes': 1024*1024*10,
            'backupCount': 10,
            'formatter': 'standard',
        },
        # Warn Level to file.
        'file_warn': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(log_dir, 'warn.log'),
            'maxBytes': 1024*1024*10,
            'backupCount': 10,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        # All basic logging.
        '': {
            'handlers': ['console', 'file_debug', 'file_info', 'file_warn'],
            'level': 'DEBUG',
            'propagate': False,
        }
    },
}


# Load dictionary of settings into logger.
logging.config.dictConfig(LOGGING)

# Test logging.
logger = get_logger(__name__)
logger.info('Logging initialized.')
logger.debug('Logging directory: ' + log_dir)
