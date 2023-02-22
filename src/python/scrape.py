from selenium import webdriver
from selenium.webdriver.common.by import By
import csv

def scrape_table(table):
    # print(table.get_attribute('outerHTML'))
    # children = table.find_elements(By.XPATH,'.//*')
    tbl = table.get_attribute('outerHTML')
    csvFile = open('editors.csv', 'a')
    writer = csv.writer(csvFile)
    csvRow = []
    try:
        csvRow.append(tbl)
        writer.writerow(csvRow)
    finally:
        csvFile.close()
