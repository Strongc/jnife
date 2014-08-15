# -*- coding: utf-8; -*-

import os
import json
import logging
import logging.config

def setup_logging(default_path='logging.json',
                  default_level=logging.INFO,
                  env_key='LOG_CFG'):
    """Setup logging configuration
    
    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    defpath= os.path.join( os.path.dirname( __file__ ), 'logging.json')
        
    if os.path.exists(path): 
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
        
    elif os.path.exists(defpath):
        with open(defpath, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
        
    else:
        logging.basicConfig(level=default_level)



setup_logging()

