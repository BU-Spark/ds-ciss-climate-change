import re
import time
import pandas as pd
import csv
from train import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

URL = "http://nychanow.nyc/issues/"
NYCHA_DATA = "src/data/NYCHA.csv"
PASS_ONE_PATH = "src/data/nychanow_pass_one.csv"
PASS_TWO_PATH = "src/data/nychanow_pass_two.csv"

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


    

""" write url, buildings, dates to csv """
def write_results(url,builidings,dates):
    with open (PASS_ONE_PATH,'a') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([url,builidings,dates])
    csvfile.close()
    
""" performs text analysis of given article """
def analyze_article(article,buildings,driver:webdriver.Chrome):
    driver.get(article)
    time.sleep(6)
    # text is divided into various p tags, so we need all of them
    p_tags = driver.find_element(By.TAG_NAME,"article").find_elements(By.TAG_NAME,"p")
    text = ""
    for p in p_tags:
        # if p tag has text, remove punc and add it 
        if p.text and not p.text.isspace():
            stripped_text = re.sub(r'[^\w\s]','',p.text)
            text += " " + stripped_text.lower()
    # check if text contains any of the NYCHA buildings
    mentioned = []
    for building in buildings:
        if building in text:
            mentioned.append(building)
    if mentioned: # if NYCHA buildings mentioned, get dates and write all data to csv
        dates = extract_dates(text)
        write_results(article,mentioned,dates)

""" what buildings did the article mention, if any? """ 
def mentioned_buildings(text):
    buildings = fetch_buildings(NYCHA_DATA)
    res = []
    for b in buildings:
        if b.upper() in text.upper():
            res.append(b)
    return res

""" collects all nychanow articles that mention any NYCHA building, writes results to csv """
def pass_one():
    # add column names to csv file
    columns = ['url','buildings','dates']
    with open (PASS_ONE_PATH,'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(columns)
    csvfile.close()

    driver = init()
    driver.get(URL)
    time.sleep(5)
    buildings = fetch_buildings(NYCHA_DATA)

    releases = driver.find_elements(By.TAG_NAME,"ul")[1].find_elements(By.TAG_NAME,"li") # list of all press releases
    urls = [release.find_element(By.TAG_NAME,"a").get_attribute("href") for release in releases] # store each url in list
    for url in urls: # start scraping each month's pr
        driver.get(url) # grab html of pr
        time.sleep(6)
        # fetch all the links on the page
        articles = driver.find_elements(By.TAG_NAME,"article")
        articles = [article.find_element(By.TAG_NAME,"a").get_attribute("href") for article in articles]
        # for each link, analyze the text for mentions of NYCHA buildings
        for article in articles:
            analyze_article(article,buildings,driver)
            time.sleep(5)

""" given a url, return the text of the article """
def retrieve_text(url):
    driver = init()
    driver.get(url)
    time.sleep(6)
    # text is divided into various p tags, so we need all of them
    p_tags = driver.find_element(By.TAG_NAME,"article").find_elements(By.TAG_NAME,"p")
    text = ""
    for p in p_tags:
        # if p tag has text, remove punc and add it 
        if p.text and not p.text.isspace():
            text += " " + p.text
    return text

""" given cleaned text of an article, return a relevancy score """
def calculate_score(text:str,score_dict:collections.defaultdict):
    score = 0
    text = text.split()
    for word in text:
        score += score_dict[word]
    return score

""" assigns relevancy scores to results from pass one """
def pass_two():
    score_dict = assign_score() # dictionary with structure { keyword: score }
    # stores scores and dates for df modification later
    scores_list = [] 
    start_dates_list = []
    end_dates_list = []
    misc_dates_list = []
    with open(PASS_ONE_PATH) as f:
        reader = csv.reader(f)
        # for each article, calculate score and extract dates
        for row in reader:
            if row and row[0] != "url":
                text = retrieve_text(row[0])
                dates = extract_dates(text)
                print(dates)
                start_dates_list.append(dates['start'])
                end_dates_list.append(dates['end'])
                misc_dates_list.append(dates['misc'])
                stopwords = init_stopwords()
                cleaned_text = clean_text(text,stopwords)
                score = calculate_score(cleaned_text,score_dict)
                scores_list.append(score)
    # add scores and dates to df, write it to a new csv file
    results = pd.read_csv(PASS_ONE_PATH)
    results['start'] = start_dates_list
    results['end'] = end_dates_list
    results['all dates'] = misc_dates_list
    results['relevance score'] = scores_list
    results = results.sort_values(by='relevance score',ascending=False)
    results.to_csv(PASS_TWO_PATH)

def __main__():
    pass_two()

""" for specific cases """
def unit_test():
    f = open("src/text/test.txt",encoding="UTF-8")
    text = f.read()
    print(extract_dates(text))

# unit_test()
__main__()