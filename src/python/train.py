import pandas as pd
import collections
import nltk
import string
from string import digits
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

TRAIN_PATH = "src/data/train.csv"

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
    print(scores)

assign_score()