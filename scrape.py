from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import pandas as pd

process = CrawlerProcess(get_project_settings())

websites = pd.read_excel('input.xlsx', sheet_name='input')['WEBSITE']
websites = websites.dropna().tolist()

if 'economictimes' in websites:
    process.crawl('economictimes')  # run economictimes scraper

if 'moneycontrol' in websites:
    process.crawl('moneycontrol')   # run moneycontrol scraper

process.start(stop_after_crawl=True)  # the script will block here until the crawling is finished

ignore = input('\n\nData Scraped. Press Enter to continue.\n\n')