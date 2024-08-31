
import time
import random
import configparser
import logging

import woffu_handler

def load_config(filename):
    config = configparser.ConfigParser()
    config.read(filename)
    return config


### Main ####
config = load_config('./user_profile.ini')

# Create and configure logger
logging.basicConfig(filename="woffu.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')



logger = logging.getLogger()


# Setting the threshold of logger to DEBUG
logger.setLevel(logging.INFO)

handler = woffu_handler.WoffuHandler(config, logger)

#webdriver = handler.load_webdriver()
handler.login()
handler.clock_in() 

#webdriver.close()


