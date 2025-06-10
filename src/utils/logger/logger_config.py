import logging
import os
from logging import config

LOG_FILE_PATH = os.path.join(os.path.dirname(__file__), 'app.log')

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'detailed': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)d] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'detailed',
            'stream': 'ext://sys.stdout',
        },
        'file': {
            'class': 'logging.FileHandler',
            'level': 'INFO',
            'formatter': 'standard',
            'filename': LOG_FILE_PATH,
            'encoding': 'utf8',
        },
        'rotating_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'formatter': 'standard',
            'filename': LOG_FILE_PATH,
            'mode': 'a',
            'maxBytes': 5 * 1024 * 1024,
            'backupCount': 5,
            'encoding': 'utf8',
        },
    },
    'loggers': {
        'app': {
            'handlers': ['console', 'rotating_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'uvicorn': {
            'handlers': ['console', 'rotating_file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['console', 'rotating_file'],
        'level': 'WARNING',
    },
}

def setup_logging():
    """Initialize logging configuration."""
    config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger('app')
    logger.debug("Logging configuration loaded successfully")
    return logger