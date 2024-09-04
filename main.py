

import argparse
import configparser
import logging
import daemon
import random
from datetime import datetime, timedelta
import time

import woffu_handler


def load_config(filename):
    config = configparser.ConfigParser()
    config.read(filename)
    return config


def parse_time(time_str):
    hours = int(time_str.split(':')[0])
    minutes = int(time_str.split(':')[1])
    time = datetime.now()
    time = time.replace(hour=hours, minute=minutes)
    return time


def run():
    # load configuration
    config = load_config('./user_profile.ini')
    CHECK_IN_TIME = parse_time(config["SCHEDULE"]["CHECK_IN_TIME"])
    CHECK_OUT_TIME = parse_time(config["SCHEDULE"]["CHECK_OUT_TIME"])

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

        if (handler.is_working_day()):
            working_day = True
        else:
            working_day = False

        currentTime = datetime.now()
        checkInTime = currentTime 
        if (currentTime >= CHECK_IN_TIME
                and currentTime.replace(hour=16) >= currentTime 
                and not checkedIn and working_day): 
            delay_mins = random.randrange(15)
            print("Delay checkin for " + str(delay_mins) + " mins.")
            time.sleep(60*delay_mins)
            handler.login()
            handler.clock_in()
            checkInTime = datetime.now()
            sleepHours = 8
            sleepMinutes = delay_mins
            checkedIn = True

        elif ((checkInTime+timedelta(hours=8)) <= currentTime and checkedIn and working_day):
            handler.login()
            handler.clock_out()
            sleepTime = 24 - currentTime.hour + CHECK_IN_TIME
            sleepMinutes = 0
            checkedIn = False

        else:
            sleepHours = abs(CHECK_IN_TIME.hour - currentTime.now().hour)
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
