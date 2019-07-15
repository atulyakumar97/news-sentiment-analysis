import pandas as pd
from datetime import datetime
import itertools
from nltk.corpus import wordnet as wn
import os

data = pd.read_csv("Scrape Output.csv")  # read output of scrape.py

inputdf = pd.read_excel('input.xlsx', sheet_name='input')  # read input
inputdf = inputdf.drop(columns='WARNING')
inputdf = inputdf.drop(columns='WARNING2')

datefrom = inputdf['DATEFROM'].dropna().tolist()[0]
dateto = inputdf['DATETO'].dropna().tolist()[0]

keywords = inputdf['KEYWORDS'].tolist()
output = pd.DataFrame(columns=['COMPANYNAME']+keywords)

searchoption = inputdf['SEARCH OPTION'].tolist()[0]

# column of dataframe, removed null values, only unique rows and converted to list
uniquecompanylist = data['COMPANYNAME'].dropna().unique().tolist()
inputcompanylist = inputdf['COMPANYNAME'].dropna().unique().tolist()

if searchoption == 'Article Content':
    searchdata = 'article'
    folder = 'Article Content Log'
elif searchoption == 'Article Title':
    searchdata = 'title'
    folder = 'Article Title Log'

for company in uniquecompanylist:
    allwords = {}
    contents = data.query("COMPANYNAME == "+'\''+company+'\'')[searchdata].tolist()  # for keyword counting
    dates = data.query("COMPANYNAME == " + '\'' + company + '\'')['date'].tolist()
    links = data.query("COMPANYNAME == " + '\'' + company + '\'')['article_link'].tolist()  # for log\company.txt

    log = []
    for date, content, link in zip(dates, contents, links):
        datetime_object = datetime.strptime(date, '%d-%m-%Y')  # Scraped string to datetime object
        if datetime_object < datefrom or datetime_object > dateto:  # between datefrom and dateto
            continue

        for word in keywords:
            similarwords = []
            for ss in wn.synsets(word):
                similarwords.append([i for i in ss.lemma_names()])  # synonyms / similar words generator

            similarwords = itertools.chain(*similarwords)   # list of lists to itertools object
            similarwords = list(similarwords)  # itertools object to list
            similarwords = similarwords + [word]  # also add original keyword incase similar words not found
            similarwords = list(dict.fromkeys(similarwords))  # remove repetitions

            for similarword in similarwords:
                if similarword in content:
                    log.append(link)    # add url of article to log
                    if word in allwords:  # if keyword has been counted once before
                        allwords[word] = allwords[word] + 1
                    else:  # if keyword is new
                        allwords[word] = 1

    for word in keywords:
        if word not in allwords:
            allwords[word] = 0  # set value if keyword not found
        else:
            pass
    finallog = []
    [finallog.append(i) for i in log if i not in finallog]  # only unique URLs in finallog
    f = open(os.path.dirname(os.path.abspath(__file__))+"\\logs\\"+folder+"\\"+company+".txt", 'w')  # open log file
    f.write('\n'.join(finallog))  # write log
    f.close()

    allwords['COMPANYNAME'] = company
    output = output.append(allwords, ignore_index=True)

from difflib import get_close_matches

threshold = pd.read_excel('input.xlsx', sheet_name='input')['THRESHOLD']
threshold = float(threshold.dropna().tolist()[0])

for i in inputcompanylist:
    allwords = {}
    if len(get_close_matches(i.upper(), uniquecompanylist, cutoff=threshold)) > 0:
        pass
    else:
        print(i.upper(), 'not matched')
        allwords['COMPANYNAME'] = i.upper()
        for word in keywords:
            allwords[word] = 'NA'   # adds NA for all keywords since company is not matched
        output = output.append(allwords, ignore_index=True)

output.to_csv('Analyse Output.csv', index=False)  # write to csv

print('\n\nProgram Developed by linkedin.com/in/atulyakumar')
ignore = input('Analyse Output.csv ready.\nPress Enter to end program.')

