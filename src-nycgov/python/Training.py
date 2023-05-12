import re
import csv
from selenium import webdriver
from bs4 import BeautifulSoup as soup
from methods import *

# read keywords and urls
keywords = readKeywords()
names, urls = readNames()
scoredict = assign_score()


def analyze_article(urls, driver: webdriver.Chrome):

    csvFile = open('training.csv', 'wt+')
    writer = csv.writer(csvFile)
    writer.writerow(["Training Dataset"])
    writer.writerow(["Article Name", "Article URL", "Keywords", "Start Date",
                     "End Date", "All Dates", "Buildings", "Scores"])

    try:
        # Open the URLs and extract the text from the articles
        for name, url in zip(names, urls):
            driver.get(url)
            s = soup(driver.page_source, 'html.parser')
            p_text = ""
            for p in s.find_all('p'):
                # remove all non-alphanumeric and non-whitespace characters
                stripped_text = re.sub(r'[^\w\s]', '', p.text)
                # append text to p_text, ignore case.
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
                # find keywords in the article body
                if re.search(r'\b' + re.escape(key) + r'\b', p_text, re.IGNORECASE):
                    print("keyword:", key)
                    print("URL", url)
                    keys.append(key)
                    if not article_name:
                        article_name.append(name)
                    # avoid recording the same url twice.
                    if not articleURL:
                        articleURL.append(url)
                    startDate = extract_start_dates(p_text)
                    print("Start Date:", startDate)
                    endDate = extract_end_dates(p_text)
                    print("End Date:", endDate)
                    allDates = extract_all_dates(p_text)
                    print("All Dates:", allDates)
                    buildings = mentioned_buildings(p_text)
                    print("Building:", buildings)
                    scores = calculate_score(p_text, scoredict)
                    print("Scores:", scores)
                    data = [article_name, articleURL, keys, startDate, endDate,
                            allDates, buildings, scores]
            if startDate or endDate or allDates:
                writer.writerow(data)
    finally:
        csvFile.close()

    input()


def __main__():
    driver = init()
    analyze_article(urls, driver)


__main__()
