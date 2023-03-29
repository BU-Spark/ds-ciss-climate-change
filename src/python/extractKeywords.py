import re
import csv
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as soup
import nltk
from nltk.corpus import stopwords
from nltk.probability import FreqDist


all_text = ""
urls = ['https://www.nyc.gov/office-of-the-mayor/news/152-16/mayor-de-blasio-dep-that-all-5-300-buildings-have-discontinued-use-most-polluting',
        'https://www.nyc.gov/site/nycha/about/press/pr-2017/nycha-begins-work-on-largest-public-housing-energy-savings-program-in-the-nation-20170406.page',
        'https://www.nyc.gov/site/nycha/about/press/pr-2017/new-lighting-announcement-20170602.page',
        'https://www.nyc.gov/site/nycha/about/press/pr-2018/pr-20181023.page',
        'https://betterbuildingssolutioncenter.energy.gov/showcase-projects/new-york-city-housing-authority-344-east-28th-street',
        'http://nychanow.nyc/105-million-in-energy-efficiency-upgrades-coming-to-15-developments/',
        'https://www.nyc.gov/site/nycha/about/press/pr-2012/nycha-begins-69-million-in-capital-improvements-and-renovations.page',
        'https://www.nyc.gov/site/nycha/about/press/pr-2016/nycha-seeks-a-partner-for-state-of-the-art-microgrid-20160622.page',
        'https://www.nyrealestatelawblog.com/manhattan-litigation-blog/2014/march/chuck-pushed-for-new-boiler-funding/',
        'https://citylimits.org/2019/10/23/climate-control-is-a-year-round-issue-at-nycha-especially-for-seniors/',
        'https://www.nyc.gov/office-of-the-mayor/news/043-18/mayor-de-blasio-dedicates-13-million-speed-nycha-response-heat-outages-replace-equipment',
        'https://www.nyc.gov/site/nycha/about/press/pr-2016/NYCHA-Reduces-Energy-Demand-Increases-Efficiency-Through-Collaboration-With-Con-Edison-20160425.page',
        'https://www.nyc.gov/site/nycha/about/press/pr-2017/howard-ave-20170511.page',
        'http://nychanow.nyc/boiler-system-upgrades-on-track-for-winter-debut/',
        'https://bklyner.com/103-million-nycha-heat-and-efficiency-investment-wont-repair-boilers/']


""" initializes selenium"""


def init():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver


def extractKeywords(urls):

    # Open the URLs and extract the text from the articles
    for url in urls:
        driver.get(url)
        s = soup(driver.page_source, 'html.parser')
        p_text = ""
        for p in s.find_all('p'):
            stripped_text = re.sub(r'[^\w\s]', '', p.text)
            p_text += " " + stripped_text.lower()
            print(p_text)
        all_text += p_text

    # create tokens
    tokens = nltk.word_tokenize(all_text)

    # save all_text to csv file
    csvFile = open('all_text.csv', 'wt+')
    writer = csv.writer(csvFile)
    try:
        writer.writerow(tokens)
    finally:
        csvFile.close()

    # remove stop words
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [token for token in tokens if not token in stop_words]
    # create frequency distribution
    fdist = FreqDist(filtered_tokens)
    print(fdist.most_common(150))


input()  # so that the window doesn't close
