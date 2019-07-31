import pandas as pd
import os

print('Program Developed by linkedin.com/in/atulyakumar\n')

inputdf = pd.read_excel('input.xlsx', sheet_name='input')

proxies = int(inputdf['ROTATING_PROXIES'].tolist()[0])

if proxies != 0:
    import urllib.request
    url = "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt"
    print("Fetching Proxies from the internet")
    proxydata = urllib.request.urlopen(url).read().decode('utf-8')
    proxydata = proxydata.split()
    proxydata = proxydata[:proxies]
    file = open('./news_spider/proxies.txt', 'w')
    proxydata = '\n'.join(proxydata)
    file.write(proxydata)
    file.close()
    print("Downloaded ./news_spider/proxies.txt\n")
else:
    open('./news_spider/proxies.txt', 'w').close()  # creating blank file for no proxies
    print('Proxies Disabled\n')

websites = inputdf['WEBSITE']
websites = websites.dropna().tolist()

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
process = CrawlerProcess(get_project_settings())

if 'economictimes' in websites:
    print('Loading economictimes crawler')
    process.crawl('economictimes')  # run economictimes scraper

if 'moneycontrol' in websites:
    print('Loading moneycontrol crawler')
    process.crawl('moneycontrol')   # run moneycontrol scraper

print()

process.start(stop_after_crawl=True)  # the script will block here until the crawling is finished

flag1 = 0
flag2 = 0

try:
    if os.path.getsize("moneycontrol.csv") == 0:
        print('No data scraped from moneycontrol')
        os.remove('moneycontrol.csv')
except:
    pass

try:
    if os.path.getsize("economictimes.csv") == 0:
        print('No data scraped from economictimes')
        os.remove('economictimes.csv')
except:
    pass

files = os.listdir()

if 'moneycontrol.csv' in files:
    mc = pd.read_csv('moneycontrol.csv')
    os.remove('moneycontrol.csv')
    flag1 = 1
if 'economictimes.csv' in files :
    et = pd.read_csv('economictimes.csv')
    os.remove('economictimes.csv')
    flag2 = 1

if flag1 == 1 and flag2 == 1:
    data = pd.concat([mc, et])
if flag1 == 1 and flag2 == 0:
    data = mc
if flag1 == 0 and flag2 == 1:
    data = et
if flag1 == 0 and flag2 == 0:
    data = pd.DataFrame()
    print('No data scraped')

try:
    data['Date'] = pd.to_datetime(data.date, format='%d-%m-%Y')
    data.sort_values(by=['COMPANYNAME', 'Date'], ascending=[True, False], inplace=True)
    data.drop(["ztemp", "Date"], axis=1, inplace=True)

except:
    pass

data.to_csv('Scrape Output.csv', index=False)  # write to csv

print('\nProgram Developed by linkedin.com/in/atulyakumar')
ignore = input('Scrape Output.csv ready.\nPress Enter to continue.')
