from typing import Any
from selenium import webdriver
from datetime import datetime
import time


class Scraper:
    """
        The base class for all scrapers
    """
    def getDriver(headless: bool=True, maximize: bool=False, loglevel: int=3, implicitlyWait: float=300) -> webdriver.Chrome:
        """
            Returns a driver
            - headless: If true, the browser will not be shown when running.
            - maximized: If true, the page will be maximized.
            - loglevel: The level of logs that will be printed to the terminal. 0 is everything, 3 is critical only.
            - implicitlyWait: The amount of seconds the driver will try to find an element until throwing an error.
        """
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
        self.status = 0
        self.isDeleted = False
    

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
    
    def setup(self) -> Any | None:
        """
            This function will be triggered once the program is loading into the manager. Use this to prepare for the actual scraper. For example, logging in, initializing scraper.
        """
        return 1
    
    def loop(self) -> Any:
        """
            This function will be called repeatedly when the specified time or interval has passed. It will return the desired contents from the webpage.
        """
        return "No loop function initialized..."
    
    def __str__(self) -> str:
        return f"{self.name}, {self.status}, {self.nextCycleTimeAt}"


class IntervalScraper(Scraper):
    """
        This scraper will execute in an interval.
    """
    def __init__(self, cycleTime=300):
        super().__init__(cycleTime)

 
class TimedScraper(Scraper):
    """
        This scraper will execute at a specific time of day.
    """
    def __init__(self, scheduleTime: datetime):
        super().__init__("--", "Time", scheduleTime)


class ScheduledScraper(Scraper):
    """
        This scraper will execute once at the specific time and day.
    """
    def __init__(self, scheduleModeTime: datetime):
        super().__init__("--", "Schedule", scheduleModeTime)
    
    def loop(self):
        return self.execute()
    
    def execute(self):
        """
            This function will be called when the desired date and time has been reached.
        """
        return "No execute function initialized..."