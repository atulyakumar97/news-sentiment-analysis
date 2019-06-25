# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()                    # Store article title (final level)
    article_link = scrapy.Field()             # Store article link (middle level)
    date = scrapy.Field()                     # Store article date (final level)
    time = scrapy.Field()                     # Store article time (final level)
    article = scrapy.Field()                  # Store article text (final level)
    companyname = scrapy.Field()              # Store company name (initial level)
    pass
