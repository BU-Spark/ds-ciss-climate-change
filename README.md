Project Setup:

    - For this project, an updated version of Python is needed (3.10.11 was used).
    - The required Python packages can all be installed with pip and are listed below:
        - Selenium for retrieval of html of NYCHA pages
        - BeautifulSoup for easier access of html elements
        - Time to insert delays between Selenium API calls so as to prevent overloading
        - CSV for writing data to .csv files
        - Pandas for data manipulation and dataframe configuration
        - re to use regular expressions to find dates in articles
        - nltk for text cleaning when creating a word scoring map
        - sklearn for classification models
        - collections for defaultdict()

File breakdown:

    - src/python:
        - NYCHA.py:
            this file scrapes demographic data for each building from this link: https://my.nycha.info/DevPortal/Home/Index/?redirectUrl=/DevPortal/Portal/DevelopmentData and writes it into data/NYCHA_BUILDING_DATA.csv
        - predict.py:
            this file reads in nycha press releases, trains a classifier model on the data, predicts whether each article is climate-change-related or not, and writes its predictions to data/predictions.csv
        - runner.py:
            see comments
        - scrape.py:
            does the actual work for NYCHA.py
        - train.py:
            all lexical-analysis-related functions
            
   - src/press
        - methods.py:
            this file contains all the methods for scraping web press articles and filter keywords. 
            
        - NYCHA_press_2010-2020.py: 
            this file contains the text analysis method for scraping articles from 2010-2020. 
        - NYCHA_press_2021-2023.py:
            this file contains the text analysis method for scraping articles from 2021-2023. 
        - Training.py: 
            this file contains the text analysis method for scraping and filtering information for the training articles provided by clients. 
        - URL2csv.py:
            this file contains a method to convert url list to csv format.
        - keywords2csv.py:
            this file contains a method to convert keyword list to csv format. 

Next Steps:

    - improve the classification model in predict.py by tuning the model, adding more training data, adding more features, etc.
    - more thorough lexical analysis for improved scores
    - add to/shorten keyword list
