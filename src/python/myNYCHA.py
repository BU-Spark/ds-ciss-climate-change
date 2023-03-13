import requests
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

# scrape the demographics and income data
building = '261'
building_name = soup(driver.page_source, 'html.parser').find(
    'option', {'value': building}).text
table_demo = soup(driver.page_source, 'html.parser').find(
    'div', {'id': 'tab_demographics'})
table_income = soup(driver.page_source, 'html.parser').find(
    'div', {'id': 'tab_household_income'})

csvFile = open('editors_rows.csv', 'wt+')
writer = csv.writer(csvFile)
data = []
data.append("Building Address")
data.append(building_name)
try:
    for td in table_demo.find_all('td'):
        data.append(td.text)

    for td in table_income.find_all('td'):
        data.append(td.text)
    writer.writerow(data)

finally: 
    csvFile.close()


input()  # so that the window doesn't close


# scrape the demographics data
# age_tables = driver.find_element(By.ID, 'tab_demographics').find_elements(By.XPATH, ".//*")  # puts each table in a list

# table_demo = soup(driver.page_source, 'html.parser').find('div', {'id':'tab_demographics'}).text
# table_income = soup(driver.page_source, 'html.parser').find('div', {'id':'tab_household_income'}).text

# Export tables to csv in the website table format
# for tr in table_demo.find_all('tr'):
#     data = []

#     for td in tr.find_all('td'):
#         data.append(td.text)
#     writer.writerow(data)

# for tr in table_income.find_all('tr'):
#     data = []

#     for td in tr.find_all('td'):
#         data.append(td.text)
#     writer.writerow(data)