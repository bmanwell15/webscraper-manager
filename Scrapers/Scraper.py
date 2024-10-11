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

        if mode == "Interval":
            self.nextCycleTimeAt = time.time() + cycleTime 
        elif mode == "Schedule":
            self.nextCycleTimeAt = scheduleModeTime.timestamp()
        elif mode == "Time":
            self.nextCycleTimeAt = scheduleModeTime.time()

        self.lastCycleTimeAt = time.time() if mode == "Interval" else "--"
        self.fileSize = 0
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

 
class TimedScraper(Scraper):
    def __init__(self, scheduleTime: datetime):
        super().__init__("--", "Time", scheduleTime)


class ScheduledScraper(Scraper):
    def __init__(self, scheduleModeTime: datetime):
        super().__init__("--", "Schedule", scheduleModeTime)
    
    def loop(self):
        return self.execute()
    
    def execute(self):
        out = "No execute function initialized..."
        return out