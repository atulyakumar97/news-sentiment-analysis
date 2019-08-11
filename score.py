import pandas as pd
from datetime import datetime
import itertools
from nltk.corpus import wordnet as wn
import os
import numpy as np

print('Program Developed by linkedin.com/in/atulyakumar\n')

try:
    print('Reading Scrape Output.csv file\n')
    data = pd.read_csv("Scrape Output.csv")  # read output of scrape.py
except:
    print('Scrape Output.csv file error')
    print('Program Developed by linkedin.com/in/atulyakumar')
    ignore = input('Analyse Output.csv ready.\nPress Enter to end program.')
    exit(0)

inputdf = pd.read_excel('input.xlsx', sheet_name='input')  # read input
inputdf.drop(['WARNING', 'WARNING2'], axis=1, inplace=True)

datefrom = inputdf['DATEFROM'].dropna().tolist()[0]
dateto = inputdf['DATETO'].dropna().tolist()[0]

negkeywords = inputdf['NEGATIVE_KEYWORDS'].dropna().tolist()
neg_len = len(negkeywords)
poskeywords = inputdf['POSITIVE_KEYWORDS'].dropna().tolist()
pos_len = len(poskeywords)

negoutput = pd.DataFrame(columns=['COMPANYNAME']+negkeywords)
posoutput = pd.DataFrame(columns=['COMPANYNAME']+poskeywords)

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

print('Counting Keywords')
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

        for word in negkeywords:
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

    for word in negkeywords:
        if word not in allwords:
            allwords[word] = 0  # set value if keyword not found
        else:
            pass
    finallog = []
    [finallog.append(i) for i in log if i not in finallog]  # only unique URLs in finallog
    f = open(os.path.dirname(os.path.abspath(__file__))+"\\logs\\"+folder+"\\negative\\"+company+".txt", 'w')  # open log file
    f.write('\n'.join(finallog))  # write log
    f.close()

    allwords['COMPANYNAME'] = company
    negoutput = negoutput.append(allwords, ignore_index=True)

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
        for word in negkeywords:
            allwords[word] = float('NaN')   # adds NA for all keywords since company is not matched
        negoutput = negoutput.append(allwords, ignore_index=True)

na_free = negoutput.dropna()
only_na = negoutput[np.invert(negoutput.index.isin(na_free.index))]
negoutput = negoutput.dropna()

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

        for word in poskeywords:
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

    for word in poskeywords:
        if word not in allwords:
            allwords[word] = 0  # set value if keyword not found
        else:
            pass
    finallog = []
    [finallog.append(i) for i in log if i not in finallog]  # only unique URLs in finallog
    f = open(os.path.dirname(os.path.abspath(__file__))+"\\logs\\"+folder+"\\positive\\"+company+".txt", 'w')  # open log file
    f.write('\n'.join(finallog))  # write log
    f.close()

    allwords['COMPANYNAME'] = company
    posoutput = posoutput.append(allwords, ignore_index=True)

if neg_len > pos_len:
    pos_adjust = neg_len/pos_len
    neg_adjust = 1
elif neg_len < pos_len:
    neg_adjust = pos_len/neg_len
    pos_adjust = 1
else:
    neg_adjust = 1
    pos_adjust = 1

pos_score = posoutput.drop('COMPANYNAME', axis=1).sum(axis=1, skipna=True) * pos_adjust
neg_score = negoutput.drop('COMPANYNAME', axis=1).sum(axis=1, skipna=True) * neg_adjust

negoutput = pd.concat([negoutput, neg_score], axis=1)
negoutput.rename(columns={0: "NEG_SCORE"}, inplace=True)
posoutput = pd.concat([posoutput, pos_score], axis=1)
posoutput.rename(columns={0: "POS_SCORE"}, inplace=True)

ratio = pd.concat([negoutput.COMPANYNAME, pos_score, neg_score], axis=1)
ratio.rename(columns={0: "POS_SCORE", 1: "NEG_SCORE"}, inplace=True)
ratio['Ratio'] = ratio['POS_SCORE']/ratio['NEG_SCORE']
ratio['Net Score'] = ratio['POS_SCORE']-ratio['NEG_SCORE']

writer = pd.ExcelWriter('Score Output.xlsx')
ratio.to_excel(writer, sheet_name='ratio', index=False)
negoutput.to_excel(writer, sheet_name='negative_counts', index=False)
posoutput.to_excel(writer, sheet_name='positive_counts', index=False)
only_na.to_excel(writer, sheet_name="Not Found", index=False)
writer.save()

print('\nProgram Developed by linkedin.com/in/atulyakumar')
ignore = input('Analyse Output.csv ready.\nPress Enter to end program.')
