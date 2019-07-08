from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())

# 'economictimes' and 'moneycontrol' is the name of one of the spiders of the project

spider = input('enter news site ET or MC : ')
if spider == 'ET':
    process.crawl('economictimes')  # run economictimes scraper
elif spider == 'MC':
    process.crawl('moneycontrol')   # run moneycontrol scraper
process.start(stop_after_crawl=True)  # the script will block here until the crawling is finished

ignore = input('\n\nData Scraped. Press Enter to continue.\n\n')