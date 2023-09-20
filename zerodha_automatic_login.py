from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
import time
import pyotp 



def get_key():
    totp_key='ENTER_YOUR_TOTP_KEY'
    twoFA=pyotp.TOTP(totp_key).now()
    return str(twoFA)





# Initialize Chrome driver instance
driver = webdriver.Chrome(service=ChromeService(executable_path=ChromeDriverManager().install()))

# Navigate to the URL
driver.get('https://kite.zerodha.com/positions/')
driver.maximize_window()


# Credientials
element=driver.find_element("xpath", '//*[@id="userid"]')
element.send_keys('USERID')#USERID
x=driver.find_element("xpath", '//*[@id="password"]')
x.send_keys('PASSWORD')#PASSWORD
button = driver.find_element('xpath','//*[@id="container"]/div/div/div/form/div[4]/button')
button.click()
time.sleep(1)

#login Finished

Code = get_key()


auth_code = driver.find_element('xpath','//*[@id="userid"]')
auth_code.send_keys(Code)




time.sleep(1)

risk_button = driver.find_element('xpath','//*[@id="app"]/div[6]/div/div/div[3]/div/div/div/button')
risk_button.click()




    

while True:
    time.sleep(10000)
