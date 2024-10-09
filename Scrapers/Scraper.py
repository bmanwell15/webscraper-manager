from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


class Scraper:

    def getDriver(headless=True, maximize=False, loglevel=3, implicitlyWait=300):
        option = webdriver.ChromeOptions()
        
        if maximize: option.add_argument("--start-maximized")

        if headless:
            option.add_argument('--headless=old')
            option.add_argument("--disable-gpu")
            option.add_argument("--disable-software-rasterizer")
        
        option.add_argument(f"--log-level={loglevel}")

        driver = webdriver.Chrome(options=option)
        driver.implicitly_wait(implicitlyWait)
        return driver


    def __init__(self, cycleTime = 300) -> None:
        self.name = "Unnamed Scraper"
        self.cycleTime = cycleTime
        self.lastLoopOutput = "No Output Made"
        self.nextCycleTimeAt = time.time() + cycleTime
        self.lastCycleTimeAt = time.time()
        self.fileSize = None
        self.core = None
        self.status = 0
    

    def _start(self):
        self.status = self.setup()
        print("Preforming first loop...")
        self.status = self.loop()[1]
    
    def setup(self):
        return 1
    
    def loop(self):
        out = "No loop function initialized..."
        return (out, 1)
    
    def __str__(self) -> str:
        return f"{self.name}, {self.status}, {self.nextCycleTimeAt}"