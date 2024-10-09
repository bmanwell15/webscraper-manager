from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from Scrapers.Scraper import Scraper
import time


class GetTime(Scraper):
    URL = "https://www.time.gov/"

    def __init__(self, cycleTime=10) -> None:
        super().__init__(cycleTime)
        self.name = "getTime"

    def setup(self):
        self.driver = Scraper.getDriver()
        self.driver.get(GetTime.URL)
    
    def loop(self):
        o = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[1]/div[5]/div/div/div[3]/div[2]/time").text
        time.sleep(5)
        return o, 1
    
    def __str__(self) -> str:
        return f"{self.name}, {self.status}, {self.nextCycleTimeAt}"