import scrapy
from ..items import NewsSpiderItem #Container Class
import re

class NewsSpider(scrapy.Spider):
    name = "economictimes"
    start_urls = [
        'https://economictimes.indiatimes.com/ilfs-investment-managers-ltd/stocksupdate/companyid-12694.cms',
        'https://economictimes.indiatimes.com/ilfs-transportation-networks-ltd/stocksupdate/companyid-31106.cms',
        'https://economictimes.indiatimes.com/ilfs-engineering-construction-company-ltd/stocksupdate/companyid-19811.cms'

    ]

    def parse(self, response):
        items = NewsSpiderItem()

        article_links=response.css(".eachStory a").xpath("@href").extract()
        titles=response.css(".eachStory a::text").extract()

        for title, article_link in zip(titles, article_links):
            items['title']=title
            goto_link="https://economictimes.indiatimes.com"+article_link
            items['article_link']=goto_link
            yield items




