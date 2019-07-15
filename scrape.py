import pandas as pd
import os

websites = pd.read_excel('input.xlsx', sheet_name='input')['WEBSITE']
websites = websites.dropna().tolist()

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
process = CrawlerProcess(get_project_settings())

if 'moneycontrol' in websites:
    process.crawl('moneycontrol')   # run moneycontrol scraper

if 'economictimes' in websites:
    process.crawl('economictimes')  # run economictimes scraper

process.start(stop_after_crawl=True)  # the script will block here until the crawling is finished

files = os.listdir()
flag1 = 0
flag2 = 0

if 'moneycontrol.csv' in files:
    mc = pd.read_csv('moneycontrol.csv')
    os.remove('moneycontrol.csv')
    flag1 = 1
if 'economictimes.csv' in files:
    et = pd.read_csv('economictimes.csv')
    os.remove('economictimes.csv')
    flag2 = 1

if flag1 == 1 and flag2 == 1:
    data = pd.concat([mc, et])
if flag1 == 1 and flag2 == 0:
    data = mc
if flag1 == 0 and flag2 == 1:
    data = et

data = data.drop(columns="ztemp")
data.to_csv('Scrape Output.csv', index=False)  # write to csv

print('\n\nProgram Developed by linkedin.com/in/atulyakumar')
ignore = input('Scrape Output.csv ready.\nPress Enter to continue.')
