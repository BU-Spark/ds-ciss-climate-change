# 2021-2023 Press Releases

import re
import csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as soup


URL = "https://www.nyc.gov/site/nycha/about/press/press-releases.page"
# Read the keywords from the CSV file using pandas
keywords_df = pd.read_csv('data/keywords.csv', header=None, names=['Keyword'])
keywords = keywords_df['Keyword'].tolist()


""" initializes selenium"""


def init():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver


""" extract start date and end date of projects in article using regex """


def extract_start_dates(text):
    startDate = re.findall(
        r'(?:  built at | built in | started in |began in | began at | began at | initiated at | launched in | launched at | kicked off in | kicked off at | established in)\d{4}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{4}', text)
    return startDate


def extract_end_dates(text):
    endDate = re.findall(
        r'(?: ended in | completed in |finished in | constructed in | upgraded in | repaired in | wrapped up in | wrapped up at | terminated in | ended at | completed at | finished at | constructed at | upgraded at | repaired at | terminated at | renovated at | renovated in )\d{4}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{4}', text)
    return endDate


""" performs text analysis of given article """


def analyze_article(url, driver: webdriver.Chrome):
    # fetch html for press release portal
    driver.get(url)
    # navigate to the class containing press articles
    devClass = soup(driver.page_source, 'html.parser').find(
        'div', {'class': 'span6 about-description'})
    url_list = []
    link_list = []
    for link_name in devClass.find_all('a'):
        # strip the leading and trailing white space
        link_list.append(link_name.text.strip())
        url_list.append(link_name['href'])

    # remove last k elements to exclude press-release-archives
    k = 11
    link_list = link_list[: len(link_list) - k]
    url_list = url_list[: len(url_list) - k]
    zip_list = zip(link_list, url_list)
    return zip_list


""" Export start and end date to csv """


def exportCSV(url, zip_list, driver: webdriver.Chrome):
    csvFile = open('press2021-2023.csv', 'wt+')
    writer = csv.writer(csvFile)
    writer.writerow(["2021-2023 Press Releases"])
    writer.writerow(["Article Name", "Article URL", "Keywords",
                    "Start Date", "End Date", "Project"])
    try:
        # click each article link
        for name, article_url in zip_list:
            driver.get(url)
            devData = driver.find_element(By.LINK_TEXT, name)
            devData.click()
            p_text = ""
            for p in soup(driver.page_source, 'html.parser').find_all('p'):
                stripped_text = re.sub(r'[^\w\s]', '', p.text)
                p_text += " " + stripped_text.lower()
            # check if text contains any of the NYCHA buildings
            article_name = []
            articleURL = []
            keys = []
            startDate = []
            endDate = []
            data = []
            for key in keywords:
                # match whole words only from keywords list
                if re.search(r'\b' + re.escape(key) + r'\b', name, re.IGNORECASE):
                    print("keyword:", key)
                    print("Article:", name)
                    print("URL", article_url)
                    keys.append(key)
                    if not article_name:
                        article_name.append(name)
                    if not articleURL:
                        articleURL.append(article_url)
                    startDate = extract_start_dates(p_text)
                    print("Start Date:", startDate)
                    endDate = extract_end_dates(p_text)
                    print("End Date:", endDate)
                    data = [article_name, articleURL, keys, startDate, endDate]
            if startDate or endDate:
                writer.writerow(data)
    finally:
        csvFile.close()

    input()  # so that the window doesn't close


def __main__():
    driver = init()
    zip_list = analyze_article(URL, driver)
    exportCSV(URL, zip_list, driver)


__main__()
