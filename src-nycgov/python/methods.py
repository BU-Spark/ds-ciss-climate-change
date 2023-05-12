import pandas as pd
import re
import collections
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

""" initializes selenium"""


def init():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver


""" extract start date and end date and all dates of projects in article using regex """


def extract_start_dates(text):
    startDate = re.findall(
        r'(?:  built at | built in | started in |began in | began at | initiated at | launched in | launched at | kicked off in | kicked off at | established in)\d{4}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{4}', text)
    return startDate


def extract_end_dates(text):
    endDate = re.findall(
        r'(?: ended in | completed in |finished in | constructed in | upgraded in | repaired in | wrapped up in | wrapped up at | terminated in | ended at | completed at | finished at | constructed at | upgraded at | repaired at | terminated at | renovated at | renovated in )\d{4}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{4}', text)
    return endDate


def extract_all_dates(text):
    allDates = re.findall(
        r'(?:\d{1,2} )?(?:Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* (?:\d{1,2}, )?\d{2,4}', text)
    allDates += re.findall(r'\d{4}', text)
    allDates_set = set()
    for date in allDates:
        if len(date) != 4:
            allDates_set.add(date)
        elif len(date) == 4 and (int(date) < 2100 and int(date) >= 1900):
            allDates_set.add(date)
    return allDates_set


""" returns list of NYCHA buildings """


def fetch_buildings(file):
    df = pd.read_csv(file)
    # Convert Building Address to lower case, and then to a list
    df["building_name"] = df["Building Address"].str.lower()
    building_names = df["building_name"].tolist()
    return building_names


""" what buildings did the article mention, if any? """


def mentioned_buildings(text):
    NYCHA_DATA = "data/NYCHA.csv"
    buildings = fetch_buildings(NYCHA_DATA)
    res = []
    for b in buildings:
        if b.upper() in text.upper():
            res.append(b)
    return res


""" read keywords """


def readKeywords():
    # Read the keywords from the CSV file using pandas
    keywords_df = pd.read_csv(
        'data/keywords.csv', header=None, names=['Keyword'])
    keywords = keywords_df['Keyword'].tolist()
    return keywords


""" read article name """


def readNames():
    names_df = pd.read_csv('data/train_data.csv',
                           usecols=[0], names=['article_name'])
    names = names_df['article_name'].tolist()
    url_df = pd.read_csv('data/train_data.csv',
                         usecols=[1], names=["article_url"])
    urls = url_df['article_url'].tolist()
    return names, urls


""" assigns a score to each keyword based on number of appearances """


def assign_score():
    # retrieve the keywords/counts and store in a list
    f = open("data/keywords_filtered.txt")
    keywords = f.read()
    f.close()
    keywords = keywords.split("\n")
    total_count = 0
    scores = collections.defaultdict(int)
    # first pass to get the total count
    for pair in keywords:
        keyword = pair[:pair.index(':')]
        num_appears = pair[pair.index(':')+1:]
        total_count += int(num_appears)
    # second pass to calculate the scores
    for pair in keywords:
        keyword = pair[:pair.index(':')]
        num_appears = pair[pair.index(':')+1:]
        scores[keyword] = int(num_appears)/total_count
    return scores


""" given cleaned text of an article, return a relevancy score """


def calculate_score(text: str, score_dict: collections.defaultdict):
    score = 0
    text = text.split()
    for word in text:
        score += score_dict[word]
    return score
