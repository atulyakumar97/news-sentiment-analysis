import pandas as pd
from datetime import datetime
import itertools
from nltk.corpus import wordnet as wn
import os
import numpy as np

try:
    data = pd.read_csv("Scrape Output.csv")  # read output of scrape.py
except:
    print('Scrape Output.csv file error')
    print('Program Developed by linkedin.com/in/atulyakumar')
    exit(0)

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

threshold = inputdf['THRESHOLD']
threshold = float(threshold.dropna().tolist()[0])

for i in inputcompanylist:
    allwords = {}
    if len(get_close_matches(i.upper(), uniquecompanylist, cutoff=threshold)) > 0:
        pass
    else:
        print(i.upper(), 'not matched')
        allwords['COMPANYNAME'] = i.upper()
        for word in keywords:
            allwords[word] = float('NaN')   # adds NA for all keywords since company is not matched
        output = output.append(allwords, ignore_index=True)

na_free = output.dropna()
only_na = output[np.invert(output.index.isin(na_free.index))]
output = output.dropna()

red = float(inputdf['N_STDDEV_RED'].dropna().tolist()[0])
amber = float(inputdf['N_STDDEV_AMBER'].dropna().tolist()[0])

means = output.iloc[:, 1:].mean(axis=0).values.tolist()
stds = output.iloc[:, 1:].std(axis=0).values.tolist()
reds = [i+j*red for i, j in zip(means, stds)]
ambers = [i+j*amber for i, j in zip(means, stds)]

meansapp = ['mean']+means
stdsapp = ['std']+stds
redsapp = ['max_red']+reds
ambersapp = ['max_amber']+ambers

alldata = pd.DataFrame(columns=output.columns, data=[meansapp, stdsapp, redsapp, ambersapp])
output = output.append(alldata, ignore_index=True)
keywords = output.columns.tolist()
keywords.remove('COMPANYNAME')

red_alert = []
amber_alert = []
green = []

for company in uniquecompanylist:
    counts = output.query("COMPANYNAME == "+'\''+company+'\'').iloc[:, 1:].values.tolist()[0]
    flag = 0
    red_keywords = []
    amber_keywords = []
    for red, count, keyword, amber in zip(reds, counts, keywords, ambers):
        if count > red:
            red_keywords.append(keyword)
            flag = 1

        if count > amber and count < red:
            amber_keywords.append(keyword)
            flag = 1

    if flag == 0:
        green.append(company)
    else:
        if red_keywords != [ ] :
            red_alert.append([company, red_keywords])
        if amber_keywords != [ ] :
            amber_alert.append([company, amber_keywords])

reddf = pd.DataFrame(red_alert, columns=['COMPANYNAME', 'KEYWORDS'])
amberdf = pd.DataFrame(amber_alert, columns=['Companyname', 'KEYWORDS'])
greendf = pd.DataFrame(green, columns=['COMPANYNAME'])

writer = pd.ExcelWriter('Analyse Output.xlsx')
output.to_excel(writer, sheet_name='stats', index=False)
reddf.to_excel(writer, sheet_name='RED', index=False)
amberdf.to_excel(writer, sheet_name='AMBER', index=False)
greendf.to_excel(writer, sheet_name='GREEN', index=False)
only_na.to_excel(writer, sheet_name="Not Found", index=False)
writer.save()

print('\n\nProgram Developed by linkedin.com/in/atulyakumar')
ignore = input('Analyse Output.csv ready.\nPress Enter to end program.')
