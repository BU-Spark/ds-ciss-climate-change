import selenium
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

URL = "http://nychanow.nyc/issues/"

def init():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver

def __main__():
    driver = init()
    driver.get(URL)
    links = driver.find_elements(By.TAG_NAME,"ul")[1].find_elements(By.TAG_NAME,"li")
    for link in links:
        # print(link.find_element(By.TAG_NAME,"a").text)
        driver.get()

__main__()