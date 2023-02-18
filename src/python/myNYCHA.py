import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://my.nycha.info/DevPortal/Portal/SelectDevelopment/261")

# navChildren = driver.find_elements(By.XPATH,"//ul[@id='nav']")
# print(navChildren)

devData = driver.find_element(By.LINK_TEXT,'Development Data')
devData.click()
input()

# URL = "https://my.nycha.info/DevPortal/Portal/SelectDevelopment/180"
# page = requests.get(URL,verify=False)

# print(page.text)