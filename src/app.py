import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import webbrowser
from webdriver_manager.chrome import ChromeDriverManager

class Bot():
    def __init__(self, email, password):
        self.options = Options()
        self.options.add_argument("--headless")
        self.email = email
        self.password = password
        self.driver = webdriver.Chrome(ChromeDriverManager(version="87.0.4280.88").install(), options=self.options)
        
    def login(self):
        base_login_url = "https://candidature.1337.ma/users/sign_in"
        self.driver.get(base_login_url)
        inputs = {
            "email": self.driver.find_element_by_xpath("//*[@id='user_email']"),
            "password": self.driver.find_element_by_xpath("//*[@id='user_password']"),
            "submit": self.driver.find_element_by_xpath("//*[@id='new_user']/div[2]/div[3]/input")
        }
        inputs["email"].send_keys(self.email)
        inputs["password"].send_keys(self.password)
        inputs["submit"].click()

    def CheckOrPool(self):
        if "meetings" not in self.driver.current_url:
            return "pool"
        else:
            return "check-in"

    def StartCheking(self):
        print(f"Checking for {self.CheckOrPool()} place...")
        place = False
        while not place:
            time.sleep(60)
            self.driver.refresh()
            if "S'inscrire" in self.driver.page_source:
                print(f"I found a {self.CheckOrPool()} place...")
                webbrowser.open("https://candidature.1337.ma/users/sign_in")
                place = True
            else:
                print("There are no place yet!")

    def close(self):
        self.driver.quit()

try:
    m = Bot(sys.argv[1],sys.argv[2])
except Exception:
    print("Usage: python app.py [EMAIL] [PASSWORD]")
else:
    m.login()
    m.StartCheking()
    m.close()
