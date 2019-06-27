from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())

# 'economictimes' is the name of one of the spiders of the project.
process.crawl('economictimes')
process.start()  # the script will block here until the crawling is finished

ignore = input()
#
# import pandas as pd
#
# data = pd.read_csv("data.csv")
# data = data.drop(columns="ztemp")
#
# input = pd.read_excel('input.xlsx', sheet_name='input')
# input = input.drop(columns='WARNING')
#
# keywords = input['KEYWORDS'].tolist()
# output = pd.DataFrame(columns=['COMPANYNAME']+keywords)
#
# uniquecompanylist = input['COMPANYNAME'].dropna().unique().tolist()
#
# for company in uniquecompanylist:
#     allwords = {}
#     articles = data.query("COMPANYNAME == "+'\''+company+'\'')['article'].tolist()
#     for article in articles:
#         for word in keywords:
#             if word in article:
#                 if word in allwords:
#                     allwords[word] = allwords[word] +1
#                 else:
#                     allwords[word] = 1
#
#     for word in keywords:
#         if word not in allwords:
#             allwords[word] = 0
#         else:
#             pass
#
#     allwords['COMPANYNAME'] = company
#     output = output.append(allwords, ignore_index=True)
#
# output.to_csv('output.csv', index=False)