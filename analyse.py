import pandas as pd
from datetime import datetime

data = pd.read_csv("data.csv")
data = data.drop(columns="ztemp")

inputdf = pd.read_excel('input.xlsx', sheet_name='input')
inputdf = inputdf.drop(columns='WARNING')

datefrom = inputdf['DATEFROM'].dropna().tolist()[0]
dateto = inputdf['DATETO'].dropna().tolist()[0]
print(type(datefrom))
print(datefrom, dateto)

keywords = inputdf['KEYWORDS'].tolist()
output = pd.DataFrame(columns=['COMPANYNAME']+keywords)

uniquecompanylist = data['COMPANYNAME'].dropna().unique().tolist()
inputcompanylist = inputdf['COMPANYNAME'].dropna().unique().tolist()

for company in uniquecompanylist:
    allwords = {}
    articles = data.query("COMPANYNAME == "+'\''+company+'\'')['article'].tolist()
    dates = data.query("COMPANYNAME == " + '\'' + company + '\'')['date'].tolist()
    for date, article in zip(dates, articles):
        datetime_object = datetime.strptime(date, '%d-%m-%Y')  # Scraped string to datetime object
        if datetime_object < datefrom or datetime_object > dateto:
            continue

        for word in keywords:
            if word in article:
                if word in allwords:
                    allwords[word] = allwords[word] + 1
                else:
                    allwords[word] = 1

    for word in keywords:
        if word not in allwords:
            allwords[word] = 0
        else:
            pass

    allwords['COMPANYNAME'] = company
    output = output.append(allwords, ignore_index=True)

from difflib import get_close_matches

threshold = pd.read_excel('input.xlsx', sheet_name='input')['THRESHOLD']
threshold = float(threshold.dropna().tolist()[0])

if len(uniquecompanylist) != len(inputcompanylist):
    print(inputcompanylist)
    print(uniquecompanylist)
    for i in inputcompanylist:
        allwords={}
        if len(get_close_matches(i.upper(), uniquecompanylist, cutoff=threshold)) > 0:
            pass
        else:
            print(i.upper(), 'not matched')
            allwords['COMPANYNAME']=i.upper()
            for word in keywords:
                allwords[word] = 'NA'
            output = output.append(allwords,ignore_index=True)

output.to_csv('output.csv', index=False)

ignore = input('\n\noutput.csv ready.Press Enter to end program.\n\n')