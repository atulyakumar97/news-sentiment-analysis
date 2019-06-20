import os

import subprocess

company_name=input("Enter company name : ")

scraping_command = "scrapy crawl"
cwd = os.path.dirname(os.path.realpath(__file__))

if company_name in ['ILFS','IL&FS', 'ilfs', 'il&fs', 'infrastructure leasing and finance services']:
    command = scraping_command + " economictimes -o links-titles.csv"

    process = subprocess.Popen(command, shell=True, cwd=cwd + "\\news_spider")
    print(process)
else:
    print("company not found")