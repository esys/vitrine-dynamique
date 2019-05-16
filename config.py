import sys

log_config = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s][%(levelname)s][%(name)s] %(message)s',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'default'
        },
    },
    'loggers': {
        'werkzeug': {
            'level': 'DEBUG',
            'handlers': ['console']
        },
        'nexityfr': {
            'level': 'DEBUG',
            'handlers': ['console']
        },
        'vitrinedynamique': {
            'level': 'DEBUG',
            'handlers': ['console']
        },
        'root': {
             'level': 'INFO',
             'handlers': ['console']
        },
    }
}
