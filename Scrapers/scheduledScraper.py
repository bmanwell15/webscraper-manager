from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from datetime import datetime
from Scrapers.Scraper import *

class Scheduled(ScheduledScraper):
    URL = "https://www.inchcalculator.com/what-is-todays-date/"

    def __init__(self):
        #                         Y     M   D   H   m   s
        super().__init__(datetime(2024, 10, 10, 16, 15, 0))

    def setup(self):
        self.driver = Scraper.getDriver()
        self.driver.get(Scheduled.URL)
    
    def execute(self):
        self.driver.refresh()
        o = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[1]/div/article/div[1]/div[1]/p/span").text
        return o