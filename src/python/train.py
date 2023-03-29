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

def analyze_text(text,keywords):
    pass

def clean_text(text,stop_words):
    text = ' '.join(remove_stopwords(text.split(),stop_words)) # stop words
    text = text.translate(str.maketrans('','',string.punctuation)) # punctuation
    text = lemmatize_words(text) # lemmatize
    text = text.translate(str.maketrans('','',digits)) # remove digits
    text = text.lower() # lowercase
    return text

def remove_stopwords(text,stop_words):
    return [t for t in text if t not in stop_words]

def __main__():
    train = pd.read_csv(TRAIN_PATH)
    keywords = collections.defaultdict(int)
    stop_words = init_stopwords()
    for text in train['text']:
        text = clean_text(text,stop_words)
        for word in text.split():
            keywords[word] += 1
    res = dict(sorted(keywords.items(),key=lambda pair: pair[1],reverse=True))
    print(res)

__main__()