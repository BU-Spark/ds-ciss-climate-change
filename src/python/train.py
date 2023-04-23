import pandas as pd
import collections
import nltk
import string
import csv
from string import digits
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from methods import *

TRAIN_PATH = "src/data/train.csv" # articles that are ONLY energy-related
TRAIN_COMPLETE_PATH = "src/data/train_complete.csv" # articles that are BOTH energy and non-energy-related
TRAIN_CREATED = 'src/data/train_created.csv' # the output of create_train() -- like train_complete but with more columns

""" functions for text analysis """
def lemmatize_words(text):
    lemmatizer = WordNetLemmatizer()
    return " ".join([lemmatizer.lemmatize(word) for word in text.split()])

def init_stopwords():
    stop_words = stopwords.words('english')
    stop_words.extend(["also", "and", "its", "bring", "got", "from", "lot", "rather", "even", "from", "but","that","in","you","who","to", "of", "become", "thats", "looking"])
    stop_words_set = set()
    for w in stop_words:
        stop_words_set.add(w)
    return stop_words

def clean_text(text,stop_words):
    text = ' '.join(remove_stopwords(text.split(),stop_words)) # stop words
    text = text.translate(str.maketrans('','',string.punctuation)) # punctuation
    text = lemmatize_words(text) # lemmatize
    text = text.translate(str.maketrans('','',digits)) # remove digits
    text = text.lower() # lowercase
    return text

def remove_stopwords(text,stop_words):
    return [t for t in text if t not in stop_words]

""" collects keywords from articles, counts their number of appearances, and writes them to txt file """
def write_keywords():
    train = pd.read_csv(TRAIN_PATH)
    keywords = collections.defaultdict(int)
    stop_words = init_stopwords()
    for text in train['text']:
        text = clean_text(text,stop_words)
        for word in text.split():
            keywords[word] += 1
    keywords = dict(sorted(keywords.items(),key=lambda pair: pair[1],reverse=True))
    f = open("src/data/keywords_unfiltered.txt",'w')
    for word in keywords:
        try:
            f.write(word+": "+str(keywords[word])+"\n")
        except:
            f.write("-: "+str(keywords[word])+"\n")
    f.close()

""" assigns a score to each keyword based on number of appearances """
def assign_score():
    # retrieve the keywords/counts and store in a list
    f = open("src/data/keywords_filtered.txt")
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

""" add columns to training data for model's use """
def create_train():
    score_dict = assign_score() # dictionary with structure { keyword: score }
    # stores scores and dates for df modification later
    scores_list = [] 
    buildings_list = []
    start_dates_list = []
    end_dates_list = []
    misc_dates_list = []
    with open(TRAIN_COMPLETE_PATH,encoding="UTF-8") as f:
        reader = csv.reader(f)
        # for each article, calculate score and extract dates/buildings
        for row in reader:
            if row and row[0] != "url":
                text = row[1]
                dates = extract_dates(text)
                # for adding dates to csv
                start_dates_list.append(dates['start'])
                end_dates_list.append(dates['end'])
                misc_dates_list.append(dates['misc'])
                # for adding score to csv
                stopwords = init_stopwords()
                cleaned_text = clean_text(text,stopwords)
                score = calculate_score(cleaned_text,score_dict)
                scores_list.append(score)
                # for adding buildings to csv
                buildings_mentioned = mentioned_buildings(text)
                buildings_list.append(buildings_mentioned)
    # add scores, buildings, and dates to df; write it to a new csv file
    results = pd.read_csv(TRAIN_COMPLETE_PATH)
    results = results.drop(['text'],axis=1) # get rid of the text column
    results['buildings'] = buildings_list
    results['start'] = start_dates_list
    results['end'] = end_dates_list
    results['all dates'] = misc_dates_list
    results['relevance score'] = scores_list
    results['no. buildings mentioned'] = results.apply(lambda row: len(row['buildings']),axis=1)
    results = results.sort_values(by='relevance score',ascending=False)
    results.to_csv(TRAIN_CREATED)

print(assign_score())