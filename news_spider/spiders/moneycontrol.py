import scrapy
from ..items import NewsSpiderItem  # Container Class
import re
from datetime import datetime
import string
import pandas as pd
from nsepy import get_history
from difflib import get_close_matches


class NewsSpider(scrapy.Spider):
    name = "moneycontrol"

    global excelinput
    global threshold

    threshold = pd.read_excel('input.xlsx', sheet_name='input')['THRESHOLD']
    threshold = float(threshold.dropna().tolist()[0])

    excelinput = pd.read_excel('input.xlsx', sheet_name='input')['COMPANYNAME']
    excelinput = excelinput.dropna().tolist()
    excelinput = [i.upper() for i in excelinput]

    # All start URLs specified for faster access
    start_urls_a = ['https://www.moneycontrol.com/india/stockpricequote/'+i for i in string.ascii_lowercase[:27]]
    start_urls_others = ['https://www.moneycontrol.com/india/stockpricequote/others']
    start_urls = start_urls_a+start_urls_others

    def parse(self, response):
        companieslist = response.css(".MT10 .bl_12::text").extract()  # Scrape list of companies beginning w/ alphabet
        companieslist = list(map(str.upper, companieslist))  # Company names to uppercase
        companieslisturl = response.css(".MT10 .bl_12").xpath("@href").extract()  # Scrape company URLs

        companiesID1 = [i.split(sep="/")[-1] for i in companieslisturl]
        companiesID2 = [re.search("^[A-Z]*",i).group()for i in companiesID1]

        # stockname = response.css(".gry10:nth-child(1)::text").extract()[1].strip().split()[1]
        print(companieslist)
        print(companieslisturl)
        print(companiesID1)
        print(companiesID2)
        yield response

# datetime.now().year
#https://www.moneycontrol.com/stocks/company_info/stock_news.php?sc_id=IDF01&scat=&pageno=2&next=0&durationType=Y&Year=2018&duration=1&news_type=