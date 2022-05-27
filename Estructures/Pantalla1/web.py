from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import pyautogui
import time
import schedule

# time. sleep(30)

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
driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')  # Optional argument, if not specified will search path.
driver.get("http://192.100.101.40:3000/d/GImp63kgk/sitja?orgId=1")
driver.maximize_window()

EMAIL_FIELD = (By.XPATH, "//body/div[@id='reactRoot']/div[1]/main[1]/div[3]/div[1]/div[2]/div[1]/div[1]/form[1]/div[1]/div[2]/div[1]/div[1]/input[1]")
WebDriverWait(driver, 20).until(EC.element_to_be_clickable(EMAIL_FIELD)).send_keys('admin')
time.sleep(1)
pyautogui.press('tab')
time.sleep(1)
pyautogui.press('1')
pyautogui.press('2')
pyautogui.press('3')
pyautogui.press('4')
pyautogui.press('5')
pyautogui.press('6')
pyautogui.press('7')
pyautogui.press('8')
pyautogui.press('9')
time.sleep(1)
# PWD_FIELD = (By.XPATH, "//body/div[@id='reactRoot']/div[1]/div[2]/div[3]/div[1]/div[2]/div[1]/div[1]/form[1]/div[2]/div[2]/div[1]/div[1]/input[1]")
# WebDriverWait(driver, 20).until(EC.element_to_be_clickable(PWD_FIELD)).send_keys('123456789')

NEXT_BTN = (By.XPATH, "//body/div[@id='reactRoot']/div[1]/main[1]/div[3]/div[1]/div[2]/div[1]/div[1]/form[1]/button[1]")
WebDriverWait(driver, 20).until(EC.element_to_be_clickable(NEXT_BTN)).click()

pyautogui.press('f11')

NEXT_BTN2 = (By.XPATH, "//div[contains(text(),'Aspiracio')]")


while True:
    try:

        WebDriverWait(driver, 20).until(EC.element_to_be_clickable(EMAIL_FIELD)).send_keys('admin')
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable(PWD_FIELD)).send_keys('123456789')
        time.sleep(3)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable(NEXT_BTN)).click()
        time.sleep(3)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable(NEXT_BTN2)).click()

    except Exception as e:
        print(e)
        time.sleep(10)

    time.sleep(3600)
    refresh()

