import scrapy
from ..items import NewsSpiderItem # Container Class

class NewsSpider(scrapy.Spider):
    name = "economictimes"
    global alphabet
    alphabet = input("Enter company's first alphabet ex. a for Apple Inc : ")

    start_urls = [
        'https://economictimes.indiatimes.com/markets/stocks/stock-quotes?ticker='+alphabet[0]
    ]

    def parse(self, response):

        companieslist = response.css('.companyList a::text').extract()
        companieslisturl = response.css('.companyList a').xpath("@href").extract()
        companyzip = zip(companieslist, companieslisturl)

        print('Select one of the following companies to fetch their information')
        sortedlist=[]
        [sortedlist.append(i.upper()) for i, j in companyzip if i[0].upper() == alphabet[0].upper()]
        sortedlist.sort()
        print(*sortedlist, sep="\n")

        companyinput = input("Enter company name : ")
        companyzip = zip(companieslist, companieslisturl)

        for i, j in companyzip:
            if i.upper() == companyinput.upper():
                 nexturl = "https://economictimes.indiatimes.com"+j.replace('/stocks/', '/stocksupdate/')
                 break

        print('Next url = '+nexturl)

        request = scrapy.Request(nexturl, callback=self.parse_company)

        yield request

    def parse_company(self, response):
        items = NewsSpiderItem()

        article_links = response.css(".eachStory a").xpath("@href").extract()
        titles = response.css(".eachStory a::text").extract()

        for title, article_link in zip(titles, article_links):
            items = NewsSpiderItem()

            goto_link = "https://economictimes.indiatimes.com" + article_link
            items['article_link'] = goto_link

            request = scrapy.Request(goto_link, callback=self.parse_article)
            request.meta['items'] = items

            yield request

    def parse_article(self, response):
        items = response.meta['items']
        article = response.css(".Normal::text").extract()
        items['title'] = response.css('.clearfix.title::text').extract()
        items['article'] = [i.replace('\n', '') for i in article]
        items['date'] = response.css(".publish_on::text").extract()

        yield items

