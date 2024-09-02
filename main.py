

import argparse
import configparser
import logging
import daemon
import random
from datetime import datetime
import time

import woffu_handler


def load_config(filename):
    config = configparser.ConfigParser()
    config.read(filename)
    return config


def run():
    # load configuration
    config = load_config('./user_profile.ini')
    CHECK_IN_TIME = int(config["SCHEDULE"]["CHECK_IN_TIME"].split(':')[0])
    CHECK_OUT_TIME = int(config["SCHEDULE"]["CHECK_OUT_TIME"].split(':')[0])

    # Create and configure logger
    logging.basicConfig(filename="woffu.log",
                        format='%(asctime)s %(message)s',
                        filemode='w')
    # Create a simple file log
    logger = logging.getLogger()
    # Setting the threshold of logger to DEBUG
    logger.setLevel(logging.INFO)
    # Create a webdriver handler for woffu webpage
    handler = woffu_handler.WoffuHandler(config, logger)

    checkedIn = False
    while True:

        currentTime = datetime.now()
        
        if (currentTime.hour >= CHECK_IN_TIME and 16 > currentTime.hour):
            delay_mins = random.randrange(20)
            time.sleep(60*delay_mins)
            handler.login()
            handler.clock_in()
            checkInTime = datetime.now().hour
            sleepHours = 8
            sleepMinutes = delay_mins
            checkedIn = True

        elif ((checkInTime+8) <= currentTime.hour and checkedIn):
            handler.login()
            handler.clock_out()
            sleepTime = 24 - currentTime.hour + CHECK_IN_TIME
            sleepMinutes = 0
            checkedIn = False

        else:
            sleepHours = abs(CHECK_IN_TIME - currentTime.now().hour)
            sleepMinutes = 0

        logger.info("sleeping for " + str(sleepHours) + " hours.")
        sleepTime = (sleepHours * 60*60) + (sleepMinutes * 60)
        time.sleep(sleepTime)


def dameon_run():
    with daemon.DaemonContext():
        run()

### MAIN ### 
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--daemon', dest='enable_daemon', action='store_true')
    parser.add_argument('--notify', dest='enable_email', action='store_true')

    args = parser.parse_args()
    if args.enable_daemon:
        daemon_run()
    else:
        run()
