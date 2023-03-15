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
    time.sleep(5)

    releases = driver.find_elements(By.TAG_NAME,"ul")[1].find_elements(By.TAG_NAME,"li") # list of all press releases
    urls = [release.find_element(By.TAG_NAME,"a").get_attribute("href") for release in releases] # store each url in list
    for url in urls: # navigate through each url
        driver.get(url)

__main__()