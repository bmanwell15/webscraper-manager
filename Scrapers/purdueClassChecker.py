from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from Scrapers.Scraper import *
from Scrapers.Libraries.Notifier import Notifier
import traceback


class ClassEnroller(IntervalScraper):
    CLASS_SUBJECT = "BIOL"
    CLASS_NUM = "205"
    TERM = "Fall"
    YEAR = "2024"

    isFoundFlag = False

    def __init__(self, cycleTime=300) -> None:
        super().__init__(cycleTime)

    def setup(self):
        self.driver: webdriver.Chrome = Scraper.getDriver(headless=False)

        self.driver.get("https://timetable.mypurdue.purdue.edu/Timetabling/gwt.jsp?page=sectioning")
        self.driver.find_element(By.ID, "username").send_keys(ClassEnroller.getUsername())
        self.driver.find_element(By.ID, "password").send_keys(ClassEnroller.getPassword())

        # For row in TERM_TABLE
        for row in self.driver.find_element(By.XPATH, "/html/body/div[6]/div/table/tbody/tr[2]/td[2]/div/table").find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr"):
            if row.text.count(ClassEnroller.TERM) and row.text.count(ClassEnroller.YEAR):
                row.click()
                break

        print(f"Selected {ClassEnroller.TERM} {ClassEnroller.YEAR}")
  

    def loop(self):
        try:
            self.driver.find_element(By.XPATH, "/html/body/span[3]/span/span[2]/span[1]/span[3]/span[2]/div/table/tbody/tr[2]/td/table/tbody/tr[2]/td/div/div/div[2]/button[1]").click() # Click "Add new Course"

            self.driver.find_element(By.XPATH, "/html/body/div[6]/div/table/tbody/tr[2]/td[2]/div/div/table/tbody/tr[1]/td/div/div[2]/input").send_keys(f"{ClassEnroller.CLASS_SUBJECT} {ClassEnroller.CLASS_NUM}")
            
            out = self.driver.find_element(By.XPATH, "/html/body/div[6]/div/table/tbody/tr[2]/td[2]/div/div/table/tbody/tr[2]/td/div/div[1]/div/table/tbody/tr[2]/td[3]/div").text # We can assume if the course number is typed, there will only be one result. Thus the find_element can be static

            if not out.count("0 /") and not ClassEnroller.isFoundFlag:
                t = time.localtime()
                currentTime = time.strftime("%H:%M", t)
                Notifier.sendEmailWithDriver(self.driver, f"There is space in {ClassEnroller.CLASS_SUBJECT} {ClassEnroller.CLASS_NUM} now ({out}) as of {currentTime}!", ClassEnroller.getEmail())

        # END IF STATEMENT
        except Exception as e:
            t = time.localtime()
            print(traceback.format_exc())
            return "Exception Caught! [" + time.strftime("%H:%M", t) + "]"

        ClassEnroller.isFoundFlag = not out.count("0 /")
        self.driver.refresh()
        return f"{ClassEnroller.CLASS_SUBJECT} {ClassEnroller.CLASS_NUM}: {out} [{int(ClassEnroller.isFoundFlag)}]"

    def getUsername():
        file = open("./Scrapers/Libraries/passwords.env", "r")
        return file.readline().removesuffix("\n")
    def getPassword():
        file = open("./Scrapers/Libraries/passwords.env", "r")
        file.readline() # Move index
        return file.readline()

    def getPhoneNumber():
        file = open("./Scrapers/Libraries/passwords.env", "r")
        file.readline() 
        file.readline() # Move index to number
        return file.readline().removesuffix("\n")
    
    def getEmail():
        file = open("./Scrapers/Libraries/passwords.env", "r")
        file.readline()
        file.readline()
        file.readline() # Move index to email
        return file.readline().removesuffix("\n")