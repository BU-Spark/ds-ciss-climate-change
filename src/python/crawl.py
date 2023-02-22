import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen('https://my.nycha.info/DevPortal/Portal/SelectDevelopment/261')
bs = BeautifulSoup(html, 'html.parser')