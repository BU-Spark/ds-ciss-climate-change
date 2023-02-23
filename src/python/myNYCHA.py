import requests
from scrape import *
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
from bs4 import BeautifulSoup as soup


# initialize selenium
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome()
driver.maximize_window()

# fetch html for single building's portal
driver.get("https://my.nycha.info/DevPortal/Portal/SelectDevelopment/261")

# navigate to the development data for that building
devData = driver.find_element(By.LINK_TEXT, 'Development Data')
devData.click()

# scrape the demographics data
# age_tables = driver.find_element(By.ID, 'tab_demographics').find_elements(By.XPATH, ".//*")  # puts each table in a list

table_demo = soup(driver.page_source, 'html.parser').find('div', {'id':'tab_demographics'}).text
table_income = soup(driver.page_source, 'html.parser').find('div', {'id':'tab_household_income'}).text


csvFile = open('editors.csv', 'wt+')
# csvFile = open('editors.csv', 'a')

writer = csv.writer(csvFile)
csvRow = []
try:
    csvRow.append(table_demo)
    writer.writerow(csvRow)
    csvRow = []
    csvRow.append(table_income)
    writer.writerow(csvRow)
finally:
    csvFile.close()



input()  # so that the window doesn't close

# print(scrape_table(age_tables[0]))
# for table in age_tables:
#     scrape_table(table)

# print(age_tables[0].get_attribute('outerHTML'))
# print(age_tables)
# scrape_table(age_tables[0])
# tbl = age_tables[0].get_attribute('outerHTML')

