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

driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', options = chrome_options)
driver.get('http:/147.45.44.203')
driver.maximize_window()

userBiomas = (By.XPATH,"//input[@id='username']")
pwdBiomas = (By.XPATH,"//input[@id='password']")
nextBiomas = (By.XPATH,"//body/div[1]/div[1]/form[1]/div[2]/input[1]")
b1Biomas = (By.XPATH,"//body/div[@id='wrapper']/div[@id='main-area']/div[@id='submenu']/div[@id='submenu-tree']/ul[1]/li[2]/ul[1]/li[1]/a[1]/span[1]")
b2Biomas = (By.XPATH,"//body/div[@id='wrapper']/div[@id='main-area']/div[@id='submenu']/div[@id='submenu-tree']/ul[1]/li[2]/ul[1]/li[1]/ul[1]/li[1]/a[1]/span[2]")
WebDriverWait(driver, 20).until(EC.element_to_be_clickable(userBiomas)).send_keys('produccio')
WebDriverWait(driver, 20).until(EC.element_to_be_clickable(pwdBiomas)).send_keys('Technotr@f!')
WebDriverWait(driver, 20).until(EC.element_to_be_clickable(nextBiomas)).click()
WebDriverWait(driver, 20).until(EC.element_to_be_clickable(b1Biomas)).click()
WebDriverWait(driver, 20).until(EC.element_to_be_clickable(b2Biomas)).click()
pyautogui.scroll(-10)   # scroll up 10 "clicks"
time.sleep(10)
#second tab (Grafana)
driver.execute_script("window.open('about:blank', 'tab2');")
driver.switch_to.window("tab2")
driver.get('http://192.100.101.40:3000/d/cw6ECjTMk/aspiracio?orgId=1&refresh=1m')
useGrafana = (By.XPATH, "//body/div[@id='reactRoot']/div[1]/div[2]/div[3]/div[1]/div[2]/div[1]/div[1]/form[1]/div[1]/div[2]/div[1]/div[1]/input[1]")
pwdGrafana = (By.XPATH, "//body/div[@id='reactRoot']/div[1]/div[2]/div[3]/div[1]/div[2]/div[1]/div[1]/form[1]/div[2]/div[2]/div[1]/div[1]/input[1]")
nextGrafana = (By.XPATH, "//span[contains(text(),'Log in')]")
WebDriverWait(driver, 20).until(EC.element_to_be_clickable(useGrafana)).send_keys('fishTank')
WebDriverWait(driver, 20).until(EC.element_to_be_clickable(pwdGrafana)).send_keys('123456789')
WebDriverWait(driver, 20).until(EC.element_to_be_clickable(nextGrafana)).click()
time.sleep(5)
#tercera tab compressors
driver.execute_script("window.open('about:blank', 'tab3');")
driver.switch_to.window("tab3")
driver.get('http://192.100.101.40:3000/d/kWrTyjoGz/compressors?orgId=1&refresh=1m')
# NEXT_BTN2 = (By.XPATH, "//div[contains(text(),'Aspiracio')]")
time.sleep(5)
driver.execute_script("window.open('about:blank', 'tab4');")
driver.switch_to.window("tab4")
driver.get('http://192.100.101.40:3000/d/fvb82Tigz/consums-i-aspiracio?orgId=1&refresh=1m')
# NEXT_BTN2 = (By.XPATH, "//div[contains(text(),'Aspiracio')]")

# time.sleep(5)
# driver.execute_script("window.open('about:blank', 'tab5');")
# driver.switch_to.window("tab5")
# driver.get('http://192.100.101.40:3000/d/fvb82Tigz/consums-i-aspiracio?orgId=1&refresh=1m')
# # NEXT_BTN2 = (By.XPATH, "//div[contains(text(),'Aspiracio')]")
time.sleep(5)

driver.execute_script("window.open('about:blank', 'tab6');")
driver.switch_to.window("tab6")
driver.get('http://192.100.101.40:3000/d/d46iY29Mz/otr?orgId=1&refresh=1m')
# NEXT_BTN2 = (By.XPATH, "//div[contains(text(),'Aspiracio')]")
time.sleep(5)
driver.execute_script("window.open('about:blank', 'tab7');")
driver.switch_to.window("tab7")
driver.get('http://192.100.101.40:3000/d/GImp63kgk/sitja?orgId=1&refresh=30s')
# NEXT_BTN2 = (By.XPATH, "//div[contains(text(),'Aspiracio')]")
time.sleep(5)

driver.execute_script("window.open('about:blank', 'tab8');")
driver.switch_to.window("tab8")
driver.get('http://192.100.101.40:3000/d/Sv9Z2sA7z/biomassa-general?orgId=1&from=now-5m&to=now')
# NEXT_BTN2 = (By.XPATH, "//div[contains(text(),'Aspiracio')]")
time.sleep(5)

genero = driver.window_handles


pestanya = 0
reset = 0
while True:
    for g in genero:
        driver.switch_to.window(g)
        refresh()
        # print(g,type(g))
        # if pestanya == 1:
        #     try:
        #         WebDriverWait(driver, 20).until(EC.element_to_be_clickable(useGrafana)).send_keys('visualitzador')
        #         WebDriverWait(driver, 20).until(EC.element_to_be_clickable(pwdGrafana)).send_keys('123456789')
        #         WebDriverWait(driver, 20).until(EC.element_to_be_clickable(nextGrafana)).click()
        #         WebDriverWait(driver, 20).until(EC.element_to_be_clickable(NEXT_BTN2)).click()
        #         reset = 1
        #     except:
        #         pass
        #     print('Ole')
        # if reset == 1 and pestanya == 2:
        #     pyautogui.press('f5')
        #     reset =0

        time.sleep(30)
        pestanya += 1
        if pestanya == 6:
            pestanya = 0