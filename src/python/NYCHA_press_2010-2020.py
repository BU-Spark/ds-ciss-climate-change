# 2010-2020 Press Releases

import re
import csv
import pandas as pd
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from bs4 import BeautifulSoup as soup


# Read URLs
URLS_df = pd.read_csv('data/URLS.csv', header=None, names=['url'])
URLS = URLS_df['url'].tolist()

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


def analyze_article(URLS, driver: webdriver.Chrome):
    # fetch html for press release portal
    for url in URLS:
        driver.get(url)
        # navigate to the class containing press articles
        devClass = soup(driver.page_source, 'html.parser').find(
            'div', {'class': 'span6 about-description'})
        article_url_list = []
        link_list = []
        for link_name in devClass.find_all('a'):
            # strip the leading and trailing white space
            link_list.append(link_name.text.strip())
            # some href links are relative paths
            if not link_name['href'].startswith("https"):
                article_url_list.append(
                    urljoin("https://www1.nyc.gov/", link_name['href']))
            else:
                article_url_list.append(link_name['href'])

        # remove last k elements to exclude press-release-archives
        k = 11
        link_list = link_list[: len(link_list) - k]
        article_url_list = article_url_list[: len(article_url_list) - k]
        zip_list = zip(link_list, article_url_list)

        csvFile = open('press2010-2020.csv', 'a')
        writer = csv.writer(csvFile)
        # add year info as divider between each table
        writer.writerow([url[43:47]])
        writer.writerow(["Article Name", "Article URL", "Keywords",
                        "Start Date", "End Date", "Project"])
        try:
            # get each article link from article_url_list, no need to click.
            for name, article_url in zip_list:
                driver.get(article_url)
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
                        # avoid recording the same article name twice.
                        if not article_name:
                            article_name.append(name)
                        # avoid recording the same url twice.
                        if not articleURL:
                            articleURL.append(article_url)
                        startDate = extract_start_dates(p_text)
                        print("Start Date:", startDate)
                        endDate = extract_end_dates(p_text)
                        print("End Date:", endDate)
                        data = [article_name, articleURL,
                                keys, startDate, endDate]
                if startDate or endDate:
                    writer.writerow(data)
        # some links are invalid
        except WebDriverException as e:
            print(f"An error occurred while processing URL {article_url}: {e}")
        finally:
            csvFile.close()
    input()  # so that the window doesn't close


def __main__():
    driver = init()
    analyze_article(URLS, driver)


__main__()

# What I completed: 1. Added URL info. 2. Fixed some bugs & Handled edge cases/errors.
# 3. scraped data from 2010-2020 press releases.
# Next steps:
# 1. Discuss with clients about the keyword list.
# 2. Ask clients for more specific needs on dates, e.g., maybe put a boundary on the years, etc.
# 3. Scrape capital projects
