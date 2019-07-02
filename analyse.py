import pandas as pd
from datetime import datetime
import itertools
from nltk.corpus import wordnet as wn
import os

data = pd.read_csv("data.csv")
data = data.drop(columns="ztemp")

inputdf = pd.read_excel('input.xlsx', sheet_name='input')
inputdf = inputdf.drop(columns='WARNING')

datefrom = inputdf['DATEFROM'].dropna().tolist()[0]
dateto = inputdf['DATETO'].dropna().tolist()[0]

keywords = inputdf['KEYWORDS'].tolist()
output = pd.DataFrame(columns=['COMPANYNAME']+keywords)

uniquecompanylist = data['COMPANYNAME'].dropna().unique().tolist()
inputcompanylist = inputdf['COMPANYNAME'].dropna().unique().tolist()

for company in uniquecompanylist:
    allwords = {}
    articles = data.query("COMPANYNAME == "+'\''+company+'\'')['article'].tolist()
    dates = data.query("COMPANYNAME == " + '\'' + company + '\'')['date'].tolist()
    links = data.query("COMPANYNAME == " + '\'' + company + '\'')['article_link'].tolist()

    log = []
    for date, article, link in zip(dates, articles, links):
        datetime_object = datetime.strptime(date, '%d-%m-%Y')  # Scraped string to datetime object
        if datetime_object < datefrom or datetime_object > dateto:
            continue

        for word in keywords:
            similarwords = []
            for ss in wn.synsets(word):
                similarwords.append([i for i in ss.lemma_names()])

            similarwords = itertools.chain(*similarwords)
            similarwords = list(similarwords)
            similarwords = similarwords + [word]
            similarwords = list(dict.fromkeys(similarwords))

            for similarword in similarwords:
                if similarword in article:
                    log.append(link)
                    if word in allwords:
                        allwords[word] = allwords[word] + 1
                    else:
                        allwords[word] = 1

    for word in keywords:
        if word not in allwords:
            allwords[word] = 0
        else:
            pass
    finallog = []
    [finallog.append(i) for i in log if i not in finallog]
    f = open(os.path.dirname(os.path.abspath(__file__))+"\\logs\\"+company+".txt", 'w')
    f.write('\n'.join(finallog))
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
            allwords[word] = 'NA'
        output = output.append(allwords, ignore_index=True)

output.to_csv('output.csv', index=False)

ignore = input('\n\noutput.csv ready.Press Enter to end program.\n\n')