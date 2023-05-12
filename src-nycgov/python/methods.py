import re
import collections
import pandas as pd
import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

URL = "http://nychanow.nyc/issues/"
NYCHA_BUILDING_DATA = "src/data/NYCHA_BUILDING_DATA.csv"
PASS_ONE_PATH = "src/data/nychanow_pass_one.csv"
PASS_TWO_PATH = "src/data/nychanow_pass_two.csv"   

# / ** 
#       GENERAL METHODS
#                          ** /

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
    df["1"] = df["1"].str.lower() 
    building_names = df.iloc[:,1].tolist()
    return building_names

""" performs text analysis of given article """
def analyze_article(article,buildings,driver:webdriver.Chrome):
    text = retrieve_text(article)
    # check if text contains any of the NYCHA buildings
    mentioned = mentioned_buildings(text)
    if mentioned: # if NYCHA buildings mentioned, get dates and write all data to csv
        dates = extract_dates(text)['misc']
        write_results(article,mentioned,dates)

""" extract and categorize all mentioned dates in article using regex """
def extract_dates(text):
    res = {} # stores the start, end, and misc dates 
    # extracting start dates
    startDate = re.findall(r'(?: started in |began in | began at | began at | initiated at | launched in | launched at | kicked off in | kicked off at | established in)\d{4}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{4}', text)
    if not startDate:
        startDate = "None"
    # extract end dates
    endDate = re.findall(r'(?: ended in | completed in |finished in | constructed in | built in | upgraded in | repaired in | wrapped up in | wrapped up at | terminated in | ended at | completed at | finished at | constructed at | built at | upgraded at | repaired at | terminated at | renovated at | renovated in )\d{4}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{4}', text)
    if not endDate:
        endDate = "None"
    # extract misc dates
    misc_dates = re.findall(r'(?:\d{1,2} )?(?:Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* (?:\d{1,2}, )?\d{2,4}',text)
    misc_dates += re.findall(r'\d{4}',text)
    # get rid of 4 digit numbers that aren't likely years
    set_misc_dates = set()
    for date in misc_dates:
        if len(date) != 4:
            set_misc_dates.add(date)
        elif len(date) == 4 and (int(date) < 2100 and int(date) >= 1900):
            set_misc_dates.add(date)
    if not set_misc_dates:
        set_misc_dates = "None"
    res["start"] = startDate
    res["end"] = endDate
    res["misc"] = set_misc_dates
    return res

""" what buildings did the article mention, if any? """ 
def mentioned_buildings(text):
    buildings = fetch_buildings(NYCHA_BUILDING_DATA)
    res = []
    for b in buildings:
        if b.upper() in text.upper():
            res.append(b)
    return res

""" given a url, return the text of the article """
def retrieve_text(url):
    driver = init()
    driver.get(url)
    time.sleep(6)
    # text is divided into various p tags, so we need all of them
    p_tags = driver.find_element(By.TAG_NAME,"article").find_elements(By.TAG_NAME,"p")
    text = ""
    for p in p_tags:
        # if p tag has text, add it
        if p.text and not p.text.isspace():
            text += " " + p.text
    return text

""" write url, buildings, dates to csv """
def write_results(url,builidings,dates):
    with open (PASS_ONE_PATH,'a') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([url,builidings,dates])
    csvfile.close()

# / ** 
#       PASS TWO METHODS
#                          ** /

""" given cleaned text of an article, return a relevancy score """
def calculate_score(text:str,score_dict:collections.defaultdict):
    score = 0
    text = text.split()
    for word in text:
        score += score_dict[word]
    return score

# / ** 
#       MODEL METHODS
#                       ** /

""" given url, retrieves headline of NYCHA article """
def get_headline(url):
    url = url[21:-1].replace('-',' ')
    return url
