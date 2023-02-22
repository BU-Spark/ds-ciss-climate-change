import requests
from scrape import *
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

# scrape the demographics data
age_tables = driver.find_element(By.ID,'tab_demographics').find_elements(By.XPATH,".//*") # puts each table in a list
for table in age_tables:
    scrape_table(table)
# print(age_tables[0].get_attribute('outerHTML'))



input() # so that the window doesn't close
