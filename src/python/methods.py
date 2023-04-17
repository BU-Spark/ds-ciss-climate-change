import re
import collections
import pandas as pd

NYCHA_DATA = "src/data/NYCHA.csv"

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

""" given cleaned text of an article, return a relevancy score """
def calculate_score(text:str,score_dict:collections.defaultdict):
    score = 0
    text = text.split()
    for word in text:
        score += score_dict[word]
    return score

""" returns list of NYCHA buildings """
def fetch_buildings(file):
    df = pd.read_csv(file)
    df["1"] = df["1"].str.lower() 
    building_names = df.iloc[:,1].tolist()
    return building_names

""" what buildings did the article mention, if any? """ 
def mentioned_buildings(text):
    buildings = fetch_buildings(NYCHA_DATA)
    res = []
    for b in buildings:
        if b.upper() in text.upper():
            res.append(b)
    return res