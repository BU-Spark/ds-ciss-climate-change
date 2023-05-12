# 2010-2020 Press Releases

import re
import csv
import pandas as pd
from urllib.parse import urljoin
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from bs4 import BeautifulSoup as soup
from methods import *

# Read URLs and keywords
URLS_df = pd.read_csv('data/URLS.csv', header=None, names=['url'])
URLS = URLS_df['url'].tolist()
keywords = readKeywords()
scoredict = assign_score()


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
                        "Start Date", "End Date", "All Dates", "Buildings", "Scores"])
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
                allDates = []
                buildings = []
                scores = []
                data = []
                for key in keywords:
                    # search article body for keywords
                    if re.search(r'\b' + re.escape(key) + r'\b', p_text, re.IGNORECASE):
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
                        allDates = extract_all_dates(p_text)
                        print("All Dates:", allDates)
                        buildings = mentioned_buildings(p_text)
                        print("Building:", buildings)
                        scores = calculate_score(p_text, scoredict)
                        print(scores)
                        data = [article_name, articleURL,
                                keys, startDate, endDate, allDates, buildings, scores]
                if startDate or endDate or allDates:
                    writer.writerow(data)
        # some links are invalid
        except WebDriverException as e:
            print(f"An error occurred while processing URL {article_url}: {e}")
        finally:
            csvFile.close()
    input()


def __main__():
    driver = init()
    analyze_article(URLS, driver)


__main__()
