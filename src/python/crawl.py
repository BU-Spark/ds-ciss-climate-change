from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

# html = urlopen('http://www.pythonscraping.com/pages/page1.html')
# bs = BeautifulSoup(html, 'html.parser')
# bs = BeautifulSoup(html.read(), 'html.parser')
# html = urlopen('https://www.pythonscraping.com/pages/warandpeace.html')
# bs = BeautifulSoup(html.read(), 'html.parser')

# nameList = bs.findAll('span', {'class': 'green'})
# for name in nameList:
#   print(name.get_text)

# html = urlopen('https://www.pythonscraping.com/pages/page3.html')
# bs = BeautifulSoup(html, 'html.parser')
# print(bs.find('img', {'src': '../img/gifts/img1.jpg'}).parent.previous_sibling.get_text())

# html = urlopen('https://my.nycha.info/DevPortal/Portal/SelectDevelopment/261')
# bs = BeautifulSoup(html, 'html.parser')
# print(bs.get_text)
# for a in bs.find_all(href=True):
#     print("Found the URL:", a['href'])




# csvFile = open('sample.csv', 'a')
# writer = csv.writer(csvFile)
# csvRow = []
# try:
#   csvRow.append(bs.find('img', {'src': '../img/gifts/img1.jpg'}).parent.previous_sibling.get_text())
#   writer.writerow(csvRow)
# finally:
#   csvFile.close()
