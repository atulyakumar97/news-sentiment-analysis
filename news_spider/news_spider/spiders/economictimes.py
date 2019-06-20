import scrapy
from ..items import NewsSpiderItem #Container Class

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
            items = NewsSpiderItem()
            items['title'] = title
            goto_link = "https://economictimes.indiatimes.com" + article_link
            items['article_link'] = goto_link

            request = scrapy.Request(goto_link, callback=self.parse_article)
            request.meta['items'] = items

            yield request

    def parse_article(self, response):
        items = response.meta['items']
        article = response.css(".Normal::text").extract()
        items['article'] = [i.replace('\n', '') for i in article]
        items['date'] = response.css(".publish_on::text").extract()
        yield items
