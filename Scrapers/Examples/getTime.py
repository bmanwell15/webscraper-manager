from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from Scrapers.Scraper import *


class GetTime(IntervalScraper):
    URL = "https://www.time.gov/"

    def __init__(self, cycleTime=10) -> None:
        super().__init__(cycleTime)

    def setup(self):
        self.driver = Scraper.getDriver()
        self.driver.get(GetTime.URL)
    
    def loop(self):
        o = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[1]/div[5]/div/div/div[3]/div[2]/time").text
        return o