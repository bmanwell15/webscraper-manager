from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from Scrapers.Scraper import Scraper
import time


class GetTime(Scraper):
    URL = "https://www.inchcalculator.com/what-is-todays-date/"

    def __init__(self, cycleTime=30) -> None:
        super().__init__(cycleTime)
        self.name = "getDate"

    def setup(self):
        self.driver = Scraper.getDriver()
        self.driver.get(GetTime.URL)
    
    def loop(self):
        self.driver.refresh()
        o = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[1]/div/article/div[1]/div[1]/p/span").text
        return o, 1
    
    def __str__(self) -> str:
        return f"{self.name}, {self.status}, {self.nextCycleTimeAt}"