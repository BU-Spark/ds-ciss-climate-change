from scrape import *
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

NYCHA_URL = "https://my.nycha.info/DevPortal/Portal"

# initialize selenium
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
    driver = init()
    buildings = fetch_buildings(driver)
    for building in buildings:
        if building:
            # print(building)    
            driver.get(NYCHA_URL+"/SelectDevelopment/"+building) # navigate to the building's portal
            time.sleep(5)
            driver.find_element(By.LINK_TEXT,'Development Data').click() # navigate to dev data for that building
            demographic_tables = driver.find_element(By.ID,'tab_demographics').find_elements(By.XPATH,".//*") # get demographic and household tables
            household_tables = driver.find_element(By.ID,'tab_household_income').find_elements(By.XPATH,".//*")
            tables = demographic_tables+household_tables
            for table in tables: # scrape each table
                scrape_table(table)
            



# # fetch html for single building's portal
# driver.get("https://my.nycha.info/DevPortal/Portal/SelectDevelopment/261")

# # navigate to the development data for that building
# devData = driver.find_element(By.LINK_TEXT,'Development Data')
# devData.click()

# # scrape the demographics data
# age_tables = driver.find_element(By.ID,'tab_demographics').find_elements(By.XPATH,".//*") # puts each table in a list


# input() # so that the window doesn't close

__main__()

