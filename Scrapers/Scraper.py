from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from datetime import datetime
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


    def __init__(self, cycleTime=300, mode="Interval", scheduleModeTime: datetime=None) -> None:
        self.name = "Unnamed Scraper"
        self.mode = mode
        self.cycleTime = cycleTime if mode == "Interval" else "--"
        self.lastLoopOutput = "No Output Made"
        self.nextCycleTimeAt = time.time() + cycleTime if mode == "Interval" else scheduleModeTime.timestamp()
        self.lastCycleTimeAt = time.time() if mode == "Interval" else "--"
        self.fileSize = None
        self.core = None
        self.status = 0
    

    def _start(self):
        self.status = self.setup()
        if self.mode == "Interval":
            print("Preforming first loop...")
            try:
                self.lastLoopOutput = self.loop()
            except:
                self.status = -1
                return
        self.status = 1
    
    def setup(self):
        return 1
    
    def loop(self):
        out = "No loop function initialized..."
        return out
    
    def __str__(self) -> str:
        return f"{self.name}, {self.status}, {self.nextCycleTimeAt}"


class IntervalScraper(Scraper):
    def __init__(self, cycleTime=300):
        super().__init__(cycleTime)


class ScheduledScraper(Scraper):
    def __init__(self, scheduleModeTime):
        super().__init__("--", "Schedule", scheduleModeTime)
    
    def loop(self):
        return self.execute()
    
    def execute(self):
        out = "No execute function initialized..."
        return out

class TimedScraper(Scraper):
    def __init__(self, scheduleTime):
        super().__init__("--", "Timed", scheduleTime)