import csv
from bs4 import BeautifulSoup as soup

def scrape_table(building_name, table_demo, table_income):
    csvFile = open('NYCHA.csv', 'a')
    writer = csv.writer(csvFile)
    writer.writerow([]) # add a blank row to separate each building table
    title = []
    title.append(building_name)
    writer.writerow(title)

    for tr in table_demo.find_all('tr'):
        data = []

        for td in tr.find_all('td'):
            data.append(td.text)
        writer.writerow(data)

    for tr in table_income.find_all('tr'):
        data = []

        for td in tr.find_all('td'):
            data.append(td.text)
        writer.writerow(data)
    # csvFile.close()
