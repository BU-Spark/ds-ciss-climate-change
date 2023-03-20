import re
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

URL = "http://nychanow.nyc/issues/"
NYCHA_DATA = "src/data/NYCHA.csv"

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
    print(article)
    driver.get(article)
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
    if mentioned:
        dates = extract_dates(text)

""" extract all mentioned dates in article using regex """
def extract_dates(text):
    dates = re.findall(r'(?:\d{1,2} )?(?:Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* (?:\d{1,2}, )?\d{2,4}',text)
    dates += re.findall(r'\d{4}',text)
    return set(dates)

""" the worker function """
def __main__():
    driver = init()
    driver.get(URL)
    time.sleep(5)
    buildings = fetch_buildings(NYCHA_DATA)

    releases = driver.find_elements(By.TAG_NAME,"ul")[1].find_elements(By.TAG_NAME,"li") # list of all press releases
    urls = [release.find_element(By.TAG_NAME,"a").get_attribute("href") for release in releases] # store each url in list
    for url in urls: # start scraping each month's pr
        driver.get(url) # grab html of pr
        time.sleep(3)
        # fetch all the links on the page
        articles = driver.find_elements(By.TAG_NAME,"article")
        articles = [article.find_element(By.TAG_NAME,"a").get_attribute("href") for article in articles]
        # for each link, analyze the text for mentions of NYCHA buildings
        for article in articles:
            analyze_article(article,buildings,driver)
            time.sleep(5)

""" for specific cases """
def unit_test():
    text = "The funding allowed the planning process for elevator replacement to begin in early April. The timeline for elevator replacement work across the 20 different sites is estimated to range from 49 months (Cassidy-Lafayette Houses) to 81 months (Marcy Houses), depending on the number of elevators that need to be replaced and the age of the relevant developments. All elevator construction work is scheduled to be completed by early December 2028."
    dates = extract_dates(text)
    print(dates)
# unit_test()
__main__()