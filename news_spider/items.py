# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()                    # Store article title (final level)
    article_link = scrapy.Field()             # Store article link (middle level 2)
    date = scrapy.Field()                     # Store article date (final level)
    time = scrapy.Field()                     # Store article time (final level)
    article = scrapy.Field()                  # Store article text (final level)
    COMPANYNAME = scrapy.Field()              # Store company name (middle level 1)
    stockname = scrapy.Field()                # Store stock name (middle level 0)
    prevclose = scrapy.Field()                # Previous day's closing stock price (final level)
    close = scrapy.Field()                    # Closing stock price (final level)
    ztemp = scrapy.Field()                    # Store any temporary data
    website = scrapy.Field()                  # Store News Website Name
    pass
