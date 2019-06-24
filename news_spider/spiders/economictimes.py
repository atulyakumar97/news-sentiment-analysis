import scrapy
from ..items import NewsSpiderItem  # Container Class
import re
from datetime import datetime
import string


class NewsSpider(scrapy.Spider):
    name = "economictimes"
    global alphabet
    alphabet = input("Enter company's first alphabet ex. a for Apple Inc : ")

    start_urls = [
        'https://economictimes.indiatimes.com/markets/stocks/stock-quotes?ticker='+alphabet[0]
    ]

    def parse(self, response):

        companieslist = response.css('.companyList a::text').extract()  # Scrape list of companies beginning w/ alphabet
        companieslisturl = response.css('.companyList a').xpath("@href").extract()  # Scrape company URLs

        print('Select one of the following companies to fetch their information')
        sortedlist = []

        # Ignore all companies that don't begin with the alphabet
        companyzip = zip(companieslist, companieslisturl)
        [sortedlist.append(i.upper()) for i, j in companyzip if i[0].upper() == alphabet[0].upper()]
        sortedlist.sort()  # Sorting alphabetically
        print(*sortedlist, sep="\n")  # Finally prints list of all companies alphabetically

        companyinput = input("Enter company name : ")  # User inputs full company name from the displayed list

        companyzip = zip(companieslist, companieslisturl)  # re-zipping
        for i, j in companyzip:
            if i.upper() == companyinput.upper():
                 next_urlend = re.search("companyid-[0-9]*.cms", j).group()  # extract ending url using regex
                 nexturl = "https://economictimes.indiatimes.com"+'/stocksupdate_news/'+next_urlend  # company news url
                 break

        print('Next url = '+nexturl)
        request = scrapy.Request(nexturl, callback=self.parse_company)  # goto company news list url scraped from above
        yield request

    def parse_company(self, response):
        items = NewsSpiderItem()

        article_links = response.css("a").xpath("@href").extract()  # scrape all article links

        for article_link in article_links:      # iterating through all article links
            if 'javascript' in article_link:
                pass                            # ignoring javascript:void(0)
            if 'plus.google' in article_link:
                pass    # Ignoring https://plus.google.com/share?url=http://economictimes.indiatimes.com/....

            else:
                items = NewsSpiderItem()

                goto_link = "https://economictimes.indiatimes.com" + article_link
                items['article_link'] = goto_link

                request = scrapy.Request(goto_link, callback=self.parse_article)
                request.meta['items'] = items

                yield request

    def parse_article(self, response):
        items = response.meta['items']

        # text cleaning
        article = response.css(".Normal::text").extract()           # Scrape article text
        article = [i.replace('\n', '') for i in article]            # newline characters replaced with ''
        article = ' '.join(article)                                 # Convert list to string
        article = article.lower()                                   # convert to lower case

        words = article.split()                                     # Split article by whitespace into words

        # remove punctuation from each word
        table = str.maketrans(' ', ' ', string.punctuation)
        stripped = [w.translate(table) for w in words]
        article = ' '.join(stripped)

        article = article.encode(encoding='ascii', errors='ignore')  # Encoding article text in

        items['article'] = article

        items['title'] = response.css('.clearfix.title::text').extract()  # Scrape title text

        dateandtimelist = response.css(".publish_on::text").extract()
        dateandtime = dateandtimelist[0]  # single item list of string

        if 'IST' in dateandtime:    # Cleaning date and time
            dateandtime = dateandtime.replace(' IST', '')
        if 'Updated' in dateandtime:
            dateandtime = dateandtime.replace('Updated: ', '')

        datetime_object = datetime.strptime(dateandtime, '%b %d, %Y, %I.%M %p')  # Scraped string to datetime object
        date = datetime_object.strftime("%d-%m-%Y")  # DD-MM-YY
        time = datetime_object.strftime("%H:%M")  # HH:MM

        items['date'] = date
        items['time'] = time

        yield items
