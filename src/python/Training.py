import re
import csv
from selenium import webdriver
from bs4 import BeautifulSoup as soup
from methods import *

# read keywords and urls
keywords = readKeywords()
urls = ['https://www.nyc.gov/office-of-the-mayor/news/152-16/mayor-de-blasio-dep-that-all-5-300-buildings-have-discontinued-use-most-polluting',
        'https://www.nyc.gov/site/nycha/about/press/pr-2017/nycha-begins-work-on-largest-public-housing-energy-savings-program-in-the-nation-20170406.page',
        'https://www.nyc.gov/site/nycha/about/press/pr-2017/new-lighting-announcement-20170602.page',
        'https://www.nyc.gov/site/nycha/about/press/pr-2018/pr-20181023.page',
        'https://betterbuildingssolutioncenter.energy.gov/showcase-projects/new-york-city-housing-authority-344-east-28th-street',
        'http://nychanow.nyc/105-million-in-energy-efficiency-upgrades-coming-to-15-developments/',
        'https://www.nyc.gov/site/nycha/about/press/pr-2012/nycha-begins-69-million-in-capital-improvements-and-renovations.page',
        'https://www.nyc.gov/site/nycha/about/press/pr-2016/nycha-seeks-a-partner-for-state-of-the-art-microgrid-20160622.page',
        'https://www.nyrealestatelawblog.com/manhattan-litigation-blog/2014/march/chuck-pushed-for-new-boiler-funding/',
        'https://citylimits.org/2019/10/23/climate-control-is-a-year-round-issue-at-nycha-especially-for-seniors/',
        'https://www.nyc.gov/office-of-the-mayor/news/043-18/mayor-de-blasio-dedicates-13-million-speed-nycha-response-heat-outages-replace-equipment',
        'https://www.nyc.gov/site/nycha/about/press/pr-2016/NYCHA-Reduces-Energy-Demand-Increases-Efficiency-Through-Collaboration-With-Con-Edison-20160425.page',
        'https://www.nyc.gov/site/nycha/about/press/pr-2017/howard-ave-20170511.page',
        'http://nychanow.nyc/boiler-system-upgrades-on-track-for-winter-debut/',
        'https://bklyner.com/103-million-nycha-heat-and-efficiency-investment-wont-repair-boilers/']

names = ['Mayor de Blasio and DEP Announce That All 5,300 Buildings Have Discontinued Use of Most Polluting Heating Oil, Leading to Significantly Cleaner Air',
         'NYCHA BEGINS WORK ON LARGEST PUBLIC HOUSING ENERGY SAVINGS PROGRAM IN THE NATION',
         'NYCHA Announces Completion of New Lighting at 18 Developments in Brooklyn, Benefitting More Than 36,000 Residents',
         'NYCHA ANNOUNCES NEW $104.6 MILLION ENERGY CONTRACT TO IMPROVE EFFICIENCY, HEATING AT 15 DEVELOPMENTS',
         'NEW YORK CITY HOUSING AUTHORITY: 344 EAST 28TH STREET',
         '$105 Million in Energy-Efficiency Upgrades Coming to 15 Developments',
         'NYCHA Begins $69 Million in Capital Improvements and Renovations',
         'NYCHA SEEKS A PARTNER FOR STATE-OF-THE-ART MICROGRID; HEAT & POWER GENERATION SYSTEM AT RED HOOK HOUSES',
         'CHUCK PUSHED FOR NEW BOILER FUNDING',
         'Climate Control is a Year-Round Issue at NYCHA, Especially for Seniors',
         'Mayor de Blasio Dedicates $13 Million to Speed NYCHA Response to Heat Outages and Replace Equipment at Hardest-Hit Buildings',
         'NYCHA REDUCES ENERGY DEMAND, INCREASES EFFICIENCY THROUGH COLLABORATION WITH CON EDISON',
         'NYCHA’S HOWARD AVENUE RECEIVES $1 MILLION ENERGY-EFFICIENCY UPGRADES AS FIRST PROJECT IN PILOT BY NEW YORK STATE WEATHERIZATION ASSISTANCE PROGRAM',
         'Boiler System Upgrades on Track for Winter Debut',
         '$103 Million NYCHA Heat and Efficiency Investment Won’t Repair Boilers']


def analyze_article(urls, driver: webdriver.Chrome):

    csvFile = open('training.csv', 'wt+')
    writer = csv.writer(csvFile)
    writer.writerow(["Training Dataset"])
    writer.writerow(["Article Name", "Article URL", "Keywords", "Start Date",
                     "End Date", "All Dates", "Buildings"])

    try:
        # Open the URLs and extract the text from the articles
        for name, url in zip(names, urls):
            driver.get(url)
            s = soup(driver.page_source, 'html.parser')
            p_text = ""
            for p in s.find_all('p'):
                # remove all non-alphanumeric and non-whitespace characters
                stripped_text = re.sub(r'[^\w\s]', '', p.text)
                # append text to p_text, ignore case.
                p_text += " " + stripped_text.lower()
            # check if text contains any of the NYCHA buildings
            article_name = []
            articleURL = []
            keys = []
            startDate = []
            endDate = []
            allDates = []
            buildings = []
            data = []
            for key in keywords:
                # find keywords in the article TITLE
                if re.search(r'\b' + re.escape(key) + r'\b', name, re.IGNORECASE):
                    print("keyword:", key)
                    print("URL", url)
                    keys.append(key)
                    if not article_name:
                        article_name.append(name)
                    # avoid recording the same url twice.
                    if not articleURL:
                        articleURL.append(url)
                    startDate = extract_start_dates(p_text)
                    print("Start Date:", startDate)
                    endDate = extract_end_dates(p_text)
                    print("End Date:", endDate)
                    allDates = extract_all_dates(p_text)
                    print("All Dates:", allDates)
                    buildings = mentioned_buildings(p_text)
                    print("Building:", buildings)
                    data = [article_name, articleURL, keys, startDate, endDate,
                            allDates, buildings]
            if startDate or endDate or allDates:
                writer.writerow(data)
    finally:
        csvFile.close()

    input()


def __main__():
    driver = init()
    analyze_article(urls, driver)


__main__()
