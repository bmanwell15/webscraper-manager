from selenium import webdriver
# from selenium.webdriver.common.keys import Keys # For clicking buttons and filling out forms
from selenium.webdriver.common.by import By # For selecting elements (plays hand in hand with 'selenium.webdriver.common.keys')
import time

class Notifier:
    """ Provides different methods for contacting devices in different ways, such as by email or calling. """

    
    VERSION = "v1.0.0"
    """ Returns the version of the class """

    def sendEmailWithDriver(driver: webdriver.Chrome, message: str, recipientEmailAddress: str) -> None:
        """
            Sends an email with an already initialized driver. The method with create a new tab, send the email, then close the tab. Note that this method can take some time to preform, and it will block the current script until completion. The email will come from the address 'no-reply@mail.text-compare.com' \n
            Args:
                * driver - The Selenium Chrome webdriver to use.
                * message - The message of the body for the email.
                * recipientEmailAddress - The reciever of the email. Make sure it is a valid email address.\n
            Special thanks to https://text-compare.com for allowing this service.
        """
        numTabs = len(driver.window_handles)
        driver.execute_script(f"window.open('https://text-compare.com/')") # number of tabs increases by one
        driver.switch_to.window(driver.window_handles[numTabs])

        driver.find_element(By.ID, "inputText1").send_keys(message)
        driver.find_element(By.ID, "inputText2").send_keys(message + ".")
        driver.find_element(By.ID, "compareButton").click()
        
        driver.find_element(By.ID, "emailComparisonButton").click()
        
        driver.find_element(By.ID, "id_email_address").send_keys(recipientEmailAddress)
        driver.find_element(By.ID, "sendComparisonButton").click()
        driver.close()
        driver.switch_to.window(driver.window_handles[numTabs - 1])


    def sendEmail(message: str, recipientEmailAddress: str) -> None:
        """
            Sends an email to the given recipient email address. Note that this method can take some time to preform, and it will block the current script until completion. This method opens a webpage and uses a service to send the email (the service was not meant to send emails). The email will come from the address 'no-reply@mail.text-compare.com' \n
            IMPORTANT: There cannot be another webdriver running in the program. Use `sendEmailWithDriver()` if a driver is already opened.\n
            Args:
                * message - The body of the email.
                * recipientEmailAddress - The reciever of the email.\n
            Special thanks to https://text-compare.com for allowing this service.
        """
        option = webdriver.ChromeOptions()
        option.add_argument('--headless=old')
        option.add_argument("--disable-gpu")
        option.add_argument("--disable-software-rasterizer")

        driver = webdriver.Chrome(options=option)
        driver.implicitly_wait(300)

        Notifier.sendEmailWithDriver(driver, message, recipientEmailAddress)
    

    def call(number: str, hangUpAfterSeconds: float=60, countryCode: int | str=1) -> None:
        """
            Calls the given number. Note that this method can take some time to preform, and it will block the current script until completion. The call will come from the number `+31 6 33 27 32 15` (The call is from the Netherlands).\n
            IMPORTANT: There cannot be another webdriver running in the program. The program will have to close the driver, call this method, then reinitialize the driver.\n
            Args:
                * number - The phone number that will be called. The number MUST be in the format `XXX-XXX-XXXX`.
                * hangUpAfterSeconds - The amount of time, in seconds, that the call will remain open before hanging up. Note that it usually takes a couple seconds to establish the call, so it is not recomended to place a value greater than `10`.
                * countryCode - The country code of for the call. The default is `1` (America). Do NOT include the '+' sign.\n
            Special thanks to https://globfone.com/call-phone/ for this service.
        """
        alertOption = webdriver.ChromeOptions()
        alertOption.add_argument("--enable-infobars")
        alertOption.add_argument("--enable-extensions")
        # alertOption.add_argument('--headless=old')
        # alertOption.add_argument("--disable-gpu")
        # alertOption.add_argument("--disable-software-rasterizer")
        alertOption.add_argument('log-level=2')

        alertOption.add_experimental_option("prefs", {
            "profile.default_content_setting_values.media_stream_mic": 1, 
            "profile.default_content_setting_values.media_stream_camera": 1,
            "profile.default_content_setting_values.geolocation": 1, 
            "profile.default_content_setting_values.notifications": 1 
        })

        alertDriver = webdriver.Chrome(options=alertOption)

        alertDriver.get("https://globfone.com/call-phone/")

        alertDriver.find_element(By.XPATH, '/html/body/div/div[1]/section[1]/div/div/div[2]/div/form/div/div[2]/div[1]/input').send_keys("Scraper Program")
        alertDriver.find_element(By.XPATH, '/html/body/div/div[1]/section[1]/div/div/div[2]/div/form/div/div[2]/div[2]/input').click()
        alertDriver.find_element(By.XPATH, '/html/body/div[1]/div[1]/section[1]/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/div[1]/div/div[2]/div[2]/input').send_keys(f"+{countryCode} {number}") # Number must be in format XXX-XXX-XXXX
        alertDriver.execute_script("window.scrollBy(0, 100);")
        alertDriver.find_element(By.XPATH, '/html/body/div[1]/div[1]/section[1]/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/div[2]/div/div[1]').click()
        time.sleep(hangUpAfterSeconds)
        alertDriver.find_element(By.XPATH, "/html/body/div/div[5]/div").click() # Hang up
        time.sleep(3)
        alertDriver.quit()
