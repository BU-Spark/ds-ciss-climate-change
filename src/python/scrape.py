import csv
from bs4 import BeautifulSoup as soup


def scrape_table(building_name, table_demo, table_income):
    # open a csv file NYCHA.csv in append mode
    csvFile = open('NYCHA.csv', 'a')
    writer = csv.writer(csvFile)
    data = []
    data.append("Building Address")
    data.append(building_name)
    try:
        # append all the data into one row with separate columns
        for td in table_demo.find_all('td'):
            data.append(td.text)

        for td in table_income.find_all('td'):
            data.append(td.text)
        # write a list of data into one row
        writer.writerow(data)

    finally:
        print(building_name)
        # csvFile.close()
