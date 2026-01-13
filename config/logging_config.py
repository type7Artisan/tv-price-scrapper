import logging.config
import os
from datetime import datetime
from .settings import LOGS_DIR

# Logging configuration
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'detailed': {
            'format': '%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'DEBUG',
            'formatter': 'detailed',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGS_DIR, f'scraper_{datetime.now().strftime("%Y%m%d")}.log'),
        },
        'error_file': {
            'level': 'ERROR',
            'formatter': 'detailed',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGS_DIR, f'error_{datetime.now().strftime("%Y%m%d")}.log'),
        },
    },
    'loggers': {
        '': {  # Root logger
            'handlers': ['console', 'file', 'error_file'],
            'level': 'DEBUG',
            'propagate': True
        },
    }
}

# Initialize logging
logging.config.dictConfig(LOGGING_CONFIG) 