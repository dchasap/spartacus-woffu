
import time
import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By


class WoffuHandler:

    def __init__(self, conf, logger):
        self.config = conf
        self.logger = logger
        self.driver = self.load_webdriver()


    def __del__(self):
        self.driver.close()


    def load_webdriver(self):
        driver_options = Options()
        #driver_options.add_argument("--headless")
        return webdriver.Firefox(driver_options)


    def login(self):
        ORG = self.config['USER']['ORG']
        EMAIL = self.config['USER']['EMAIL']
        PASSWORD = self.config['USER']['PASSWORD']

        self.driver.get("https://" + ORG + ".woffu.com/#/login")
        #time.sleep(10)
        #print(driver.page_source)

        email = self.driver.find_element(by=By.ID, value="tuEmail")
        password = self.driver.find_element(by=By.ID, value="tuPassword")

        email.send_keys(EMAIL)
        password.send_keys(PASSWORD)

        self.driver.find_element(by=By.XPATH, value='//*[@id="intro"]/div/form/span/button').click()


    def is_working_day(self):
        #TODO: get working days from woffu site 
        weekday = datetime.datetime.today().weekday()
        if weekday < 5:
            return True

        return False


    def clock_in(self):
        if self.is_working_day():
            #TODO: Introduce some random minutes variation for clocking in
            time.sleep(10)
            #print(driver.page_source)
            self.driver.find_element(by=By.XPATH, value="//*[@class='sc-llcuoN jbETVX']").click()
            self.logger.info("Logged in.")
            #TODO: Maybe set an event to logout in 8 hours

    def clock_out(self):
        #TODO:
        return
