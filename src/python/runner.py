import time
import pandas as pd
import csv
from train import *
from methods import *

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
    buildings = fetch_buildings(NYCHA_BUILDING_DATA)

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