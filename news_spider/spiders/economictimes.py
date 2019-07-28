import scrapy
from ..items import NewsSpiderItem  # Container Class
import re
from datetime import datetime, timedelta
import string
import pandas as pd
from nsepy import get_history
from difflib import get_close_matches
count = 0


class NewsSpider(scrapy.Spider):
    name = "economictimes"
    global excelinput
    global threshold

    inputdf = pd.read_excel('input.xlsx', sheet_name='input')

    threshold = inputdf['THRESHOLD']
    threshold = float(threshold.dropna().tolist()[0])

    excelinput = inputdf['COMPANYNAME']
    excelinput = excelinput.dropna().tolist()
    excelinput = [i.upper() for i in excelinput]

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
            if len(get_close_matches(k.upper(), companieslist, cutoff=threshold)) > 0:

                closest_match = get_close_matches(k.upper(), companieslist, cutoff=threshold)[0]

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
        stockname = response.css("meta").xpath("@content").extract()[3][:-2]
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
                #items['article_link'] = goto_link

                goto_link = "https://economictimes.indiatimes.com" + article_link
                request = scrapy.Request(goto_link, callback=self.parse_article)
                request.meta['items'] = items

                yield request

    def parse_article(self, response):
        items = response.meta['items']
        items['article_link'] = response.request.url
        # text cleaning
        article = response.css(".Normal::text").extract()           # Scrape article text
        article = [i.replace('\n', '') for i in article]            # newline characters replaced with ''
        article = ' '.join(article)                                 # Convert list to string
        article = article.lower()                                   # convert to lower case

        punct = set(string.punctuation)
        finalarticle = ''

        for i in article:
            if i in punct:
                finalarticle = finalarticle + ' '
            else:
                finalarticle = finalarticle + i

        items['article'] = finalarticle.encode(encoding='ascii', errors='ignore')  # Encoding article text in

        title = response.css('.clearfix.title::text').extract()[0]  # Scrape title text
        title = title.lower()

        finaltitle = ''

        for i in title:
            if i in punct:
                finaltitle = finaltitle + ' '
            else:
                finaltitle = finaltitle + i

        items['title'] = finaltitle.encode(encoding='ascii', errors='ignore')

        dateandtimelist = response.css(".publish_on::text").extract()
        dateandtime = dateandtimelist[0]  # single item list of string

        if 'IST' in dateandtime:    # Cleaning date and time
            dateandtime = dateandtime.replace(' IST', '')
        if 'Updated' in dateandtime:
            dateandtime = dateandtime.replace('Updated: ', '')

        datetime_object = datetime.strptime(dateandtime, '%b %d, %Y, %I.%M %p')  # Scraped string to datetime object
        date = datetime_object.strftime("%d-%m-%Y")  # DD-MM-YY

        yesterday = datetime_object.date() - timedelta(days=1)

        items['date'] = date
        items['time'] = datetime_object.strftime("%H:%M")  # HH:MM

        try:
            stockdata = get_history(symbol=items['stockname'], start=datetime_object.date(), end=datetime_object.date())
            items['close'] = stockdata['Close'][0]
        except:
            items['close'] = 'NA'

        try:
            stockdata = get_history(symbol=items['stockname'], start=yesterday, end=yesterday)
            items['prevclose'] = stockdata['Close'][0]
        except:
            items['prevclose'] = 'NA'

        items['ztemp']=''
        items['website'] = 'economictimes'

        global count
        count = count + 1

        if count % 10 == 0:
            print('Update : Scraped '+str(count)+' articles from economictimes')

        if count == 0:
            print('No articles from economictimes downloaded')
        yield items
