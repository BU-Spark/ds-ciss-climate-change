import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

# initialize selenium
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome()
driver.maximize_window()

# fetch html for single building's portal
driver.get("https://my.nycha.info/DevPortal/Portal/SelectDevelopment/261")

# navigate to the development data for that building
devData = driver.find_element(By.LINK_TEXT,'Development Data')
devData.click()

# navigate to demographics tab
demographics = driver.find_element(By.XPATH,"//html").get_attribute('outerHTML')
demographics = driver.find_element(By.LINK_TEXT,'Demographics')
demographics.click()

# scrape the demographics data



input() # so that the window doesn't close
