from selenium import webdriver
from selenium.webdriver.common.by import By

def scrape_table(table):
    # print(table.get_attribute('outerHTML'))
    children = table.find_elements(By.XPATH,'.//*')
    for child in children:
        print("\n"+child.get_attribute('outerHTML'))