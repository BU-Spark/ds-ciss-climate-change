import re
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as soup
import csv


URL = "https://www.nyc.gov/site/nycha/about/press/press-releases.page"
NYCHA_DATA = "python/NYCHA.csv"
keywords = [
    "energy",
    "heating",
    "water",
    "heat",
    "boilers",
    "air",
    "sustainability",
    "reduce",
    "efficiency",
    "hot",
    "lighting",
    "quality",
    "oil",
    "steam",
    "costs",
    "savings",
    "boiler",
    "service",
    "emissions",
    "cost",
    "repairs",
    "repair",
    "performance",
    "greenhouse",
    "gas",
    "commitment",
    "conservation",
    "largest",
    "upgrade",
    "apartments",
    "replacement",
    "fuel",
    "carbon",
    "initiative",
    "power",
    "reduction",
    "climate",
    "services",
    "homes",
    "environmental"
]

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


""" extract start date and end date of projects in article using regex """


def extract_start_dates(text):
    startDate = re.findall(
        r'(?: started in |began in | began at | began at | initiated at | launched in | launched at | kicked off in | kicked off at | established in)\d{4}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{4}', text)
    return startDate


def extract_end_dates(text):
    endDate = re.findall(
        r'(?: ended in | completed in |finished in | constructed in | built in | upgraded in | repaired in | wrapped up in | wrapped up at | terminated in | ended at | completed at | finished at | constructed at | built at | upgraded at | repaired at | terminated at | renovated at | renovated in )\d{4}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{4}', text)
    return endDate


""" performs text analysis of given article """


def analyze_article(url, driver: webdriver.Chrome):
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

    csvFile = open('press.csv', 'wt+')
    writer = csv.writer(csvFile)
    writer.writerow(["Article Name", "Keywords",
                    "Start Date", "End Date", "Project"])
    try:
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
            article_name = []
            keys = []
            startDate = []
            endDate = []
            data = []
            for key in keywords:
                # match whole words only from keywords list
                if re.search(r'\b' + re.escape(key) + r'\b', name, re.IGNORECASE):
                    print("keyword:", key)
                    print("Article:", name)
                    keys.append(key)
                    article_name.append(name)
                    startDate = extract_start_dates(p_text)
                    print("Start Date:", startDate)
                    endDate = extract_end_dates(p_text)
                    print("End Date:", endDate)
                    data = [article_name, keys, startDate, endDate]
            if startDate or endDate:
                writer.writerow(data)
    finally:
        csvFile.close()

    input()  # so that the window doesn't close


def __main__():
    driver = init()
    driver.get(URL)
    time.sleep(5)
    # buildings = fetch_buildings(NYCHA_DATA)
    # this function only work with the current 2021-2023 press url
    analyze_article(URL, driver)


__main__()

# What I completed: 1. Exported 2021-2023 presses' start/end dates, project, article, and
# keywords into csv file. 2. Modified extract_dates function
# Next Steps: 1. Discuss with clients about the keyword list.
# 2. scrape data from 2010-2020 press releases.
# 3. Scrape capital projects
