from scrape import *
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup as soup

NYCHA_URL = "https://my.nycha.info/DevPortal/Portal"

def init():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver

def fetch_buildings(driver):
    driver.get(NYCHA_URL)
    time.sleep(5)
    buildings = [building.get_attribute('value') for building in driver.find_element(By.ID,'DevNum').find_elements(By.XPATH,'.//*')] # put all building ids in a list
    return buildings

def __main__():
    with open("NYCHA.csv",'r+') as file:
        file.truncate(0)
    file.close()
    driver = init()
    buildings = fetch_buildings(driver)
    for building in buildings:
        if building: 
            driver.get(NYCHA_URL+"/SelectDevelopment/"+building) # navigate to the building's portal
            time.sleep(5)
            driver.find_element(By.LINK_TEXT,'Development Data').click() # navigate to dev data for that building
            building_name = soup(driver.page_source, 'html.parser').find('option', {'value': building}).text
            table_demo = soup(driver.page_source, 'html.parser').find('div', {'id':'tab_demographics'})
            table_income = soup(driver.page_source, 'html.parser').find('div', {'id':'tab_household_income'})
            # handle the exception when there's no development data for the building
            if (not building_name or not table_demo or not table_income):
                continue
            scrape_table(building_name, table_demo, table_income)
            
__main__()