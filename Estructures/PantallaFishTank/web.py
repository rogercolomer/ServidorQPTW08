from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import pyautogui
import time
import schedule

def refresh():
    pyautogui.press('f5')

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('prefs', {
    'credentials_enable_service': False,
    'profile': {
        'password_manager_enabled': False
    }
})
driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', options = chrome_options)  # Optional argument, if not specified will search path.
driver.get('http://192.100.101.25:3000/d/NxIGfIAMk/pintura?orgId=3&refresh=1m')
driver.maximize_window()
# time.sleep(5) # Let the user actually see something!
# search_box = driver.find_element_by_name('q')
# search_box.send_keys('ChromeDriver')
# search_box.submit()
# time.sleep(5) # Let the user actually see something!

EMAIL_FIELD = (By.XPATH, "//body/grafana-app[1]/div[1]/div[1]/react-container[1]/div[1]/div[1]/div[2]/div[1]/div[1]/form[1]/div[1]/div[2]/div[1]/div[1]/input[1]")

WebDriverWait(driver, 20).until(EC.element_to_be_clickable(EMAIL_FIELD)).send_keys('planta')
PWD_FIELD = (By.XPATH, "//body/grafana-app[1]/div[1]/div[1]/react-container[1]/div[1]/div[1]/div[2]/div[1]/div[1]/form[1]/div[2]/div[2]/div[1]/div[1]/input[1]")
WebDriverWait(driver, 20).until(EC.element_to_be_clickable(PWD_FIELD)).send_keys('1111')

NEXT_BTN = (By.XPATH, "//body/grafana-app[1]/div[1]/div[1]/react-container[1]/div[1]/div[1]/div[2]/div[1]/div[1]/form[1]/button[1]")
WebDriverWait(driver, 20).until(EC.element_to_be_clickable(NEXT_BTN)).click()

pyautogui.press('f11')

schedule.every(5).minutes.do(refresh)


while True:
    schedule.run_pending()
    time.sleep(1)


