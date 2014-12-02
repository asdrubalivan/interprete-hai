import logging

import logging.config

logger = logging.getLogger(__name__)

# load config from file 
# logging.config.fileConfig('logging.ini', disable_existing_loggers=False)
# or, for dictConfig
logging.config.dictConfig({
    'version': 1,              
    'disable_existing_loggers': False,  # this fixes the problem
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: (%(filename)s -> %(funcName)s -> %(lineno)s ) : %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level':'DEBUG',    
            'class':'logging.handlers.RotatingFileHandler',
            'filename':'log.log',
            'formatter':'standard',
            'encoding':'utf8',
            'maxBytes':1200000,
        },  
    },
    'loggers': {
        '': {                  
            'handlers': ['default'],        
            'level': 'DEBUG',  
            'propagate': True
        }
    }
})

logger.info('It works!')
