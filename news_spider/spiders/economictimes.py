import scrapy
from ..items import NewsSpiderItem  # Container Class
import re
from datetime import datetime
import string
import pandas as pd
from nsepy import get_history
from difflib import get_close_matches

class NewsSpider(scrapy.Spider):
    global excelinput

    excelinput = pd.read_excel('input.xlsx', sheet_name='input')['COMPANYNAME']
    excelinput = excelinput.dropna().tolist()
    excelinput = [i.upper() for i in excelinput]

    name = "economictimes"

    # All start URLs specified for faster access
    start_urls_a = ['https://economictimes.indiatimes.com/markets/stocks/stock-quotes?ticker='+i for i in string.ascii_lowercase[:27]]
    start_urls_0 = ['https://economictimes.indiatimes.com/markets/stocks/stock-quotes?ticker='+str(i) for i in list(range(1, 10))]
    start_urls = start_urls_a+start_urls_0

    def parse(self, response):

        companieslist = response.css('.companyList a::text').extract()  # Scrape list of companies beginning w/ alphabet
        companieslist = list(map(str.upper, companieslist))
        companieslisturl = response.css('.companyList a').xpath("@href").extract()  # Scrape company URLs
        nextjump = []

        for k in excelinput:
            if len(get_close_matches(k, companieslist, cutoff=0.65)) > 0:

                closest_match = get_close_matches(k, companieslist, cutoff=0.65)[0]

                for i, j in zip(companieslist, companieslisturl):
                    if closest_match == i:
                         next_urlend = re.search("companyid-[0-9]*.cms", j).group()  # extract ending url using regex
                         nexturl1 = "https://economictimes.indiatimes.com"+j
                         nexturl2 = "https://economictimes.indiatimes.com"+'/stocksupdate_news/'+next_urlend  # company news url
                         nextjump.append([i, nexturl1, nexturl2])

        for next in nextjump:
            items = NewsSpiderItem()
            items['COMPANYNAME'] = next[0]
            items['ztemp'] = next[2]

            request = scrapy.Request(next[1], callback=self.parse_stock)
            request.meta['items'] = items
            yield request

    def parse_stock(self, response):
        items = response.meta['items']
        stockname = response.css("title::text").extract()[0].split()[0]
        items['stockname'] = stockname

        ztemp = items['ztemp']

        request = scrapy.Request(ztemp, callback=self.parse_company)
        request.meta['items'] = items

        yield request

    def parse_company(self, response):

        article_links = response.css("a").xpath("@href").extract()  # scrape all article links

        for article_link in article_links:      # iterating through all article links
            if 'javascript' in article_link or 'plus.google' in article_link:
                pass    # Ignoring https://plus.google.com/share?url=http://economictimes.indiatimes.com/....
            elif 'economictimes.indiatimes.com' in article_link:
                pass
            else:
                items = response.meta['items']

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

        title = response.css('.clearfix.title::text').extract()[0]  # Scrape title text
        items['title'] = title.encode(encoding='ascii', errors='ignore')

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

        try:
            stockdata = get_history(symbol=items['stockname'], start=datetime_object.date(), end=datetime_object.date())
            items['close']=stockdata['Close'][0]
            items['prevclose']=stockdata['Prev Close'][0]
        except:
            items['close'] = 'NA'
            items['prevclose'] = 'NA'

        items['ztemp']=''
        yield items
