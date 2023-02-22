import requests
from scrape import *
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv

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
# print(age_tables[0])
# print(scrape_table(age_tables[0]))

# initialize the csvFile
csvFile = open('editors.csv', 'wt+')
writer = csv.writer(csvFile)
csvRow = ['NYCHA']
try:
    writer.writerow(csvRow)
finally:
    csvFile.close()

for table in age_tables:
    scrape_table(table)

input() # so that the window doesn't close


# print(age_tables[0].get_attribute('outerHTML'))
# print(age_tables)
# scrape_table(age_tables[0])
# tbl = age_tables[0].get_attribute('outerHTML')

# csvFile = open('editors.csv', 'wt+')
# writer = csv.writer(csvFile)
# csvRow = []
# try:
#     csvRow.append(tbl)
#     writer.writerow(csvRow)
# finally:
#     csvFile.close()


