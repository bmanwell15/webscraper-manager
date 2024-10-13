from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from datetime import datetime
from Scrapers.Scraper import *

class Timed(TimedScraper):
    URL = "https://www.time.gov/"

    def __init__(self):
        super().__init__(datetime(2024, 10, 10, 20, 42))

    def setup(self):
        self.driver = Scraper.getDriver()
        self.driver.get(Timed.URL)
    
    def loop(self):
        o = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[1]/div[5]/div/div/div[3]/div[2]/time").text
        return o