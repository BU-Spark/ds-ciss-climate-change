import re
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as soup

URL = "https://www.nyc.gov/site/nycha/about/press/press-releases.page"
NYCHA_DATA = "python/NYCHA.csv"

""" initializes selenium"""
def init():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver


""" returns list of NYCHA buildings """
def fetch_buildings(file):
    df = pd.read_csv(file)
    # Convert Building Address to lower case, and then to a list
    df["building_name"] = df["Building Address"].str.lower()
    building_names = df["building_name"].tolist()
    return building_names
    # print(building_names)


""" extract all mentioned dates in article using regex """
def extract_dates(text):
    # ooks for dates in the format of "Month Day, Year" or "Day Month Year" and also four-digit years. 
    dates = re.findall(
        r'(?:\d{1,2} )?(?:Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* (?:\d{1,2}, )?\d{2,4}', text)
    dates += re.findall(r'\d{4}', text)
    # save dates to a set to avoid duplicates
    return set(dates)


""" performs text analysis of given article """
def analyze_article(url, buildings, driver: webdriver.Chrome):
    # fetch html for press release portal
    driver.get(url)
    # navigate to the class containing press articles
    devClass = soup(driver.page_source, 'html.parser').find(
        'div', {'class': 'span6 about-description'})
    link_list = []
    for link_name in devClass.find_all('a'):
        # strip the leading and trailing white space
        link_list.append(link_name.text.strip())

    # remove last k elements to exclude press-release-archives
    k = 11
    link_list = link_list[: len(link_list) - k]
    # print(link_list)

    # click each article link
    for name in link_list:
        driver.get(URL)
        devData = driver.find_element(By.LINK_TEXT, name)
        devData.click()
        p_text = ""
        for p in soup(driver.page_source, 'html.parser').find_all('p'):
            stripped_text = re.sub(r'[^\w\s]', '', p.text)
            p_text += " " + stripped_text.lower()
        # check if text contains any of the NYCHA buildings
        mentioned = []
        for building in buildings:
            if building in p_text:
                mentioned.append(building)
        if mentioned:
            dates = extract_dates(p_text)
    input()  # so that the window doesn't close


def __main__():
    driver = init()
    driver.get(URL)
    time.sleep(5)
    buildings = fetch_buildings(NYCHA_DATA)
    # this function only work the current url
    analyze_article(URL, buildings, driver)


__main__()

# What I completed: 1. Scrape date info from the current URL for 2021-2023 press releases.
# 2. Saved building mentioned and dates.
# Next Steps: 1. Save building and dates side by side in csv file.
# 2. scrape data from 2010-2020 press releases.
# 3. extract_dates(text) function may need modification to suit for press scraping.
# 4. Scrape capital projects