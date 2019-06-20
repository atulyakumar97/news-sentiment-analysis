import os
import subprocess
import time

company_name=input("Enter company name : ")

cwd = os.path.dirname(os.path.realpath(__file__))
if company_name+".csv" in os.listdir(cwd+"/news_spider/"):
    print(company_name+".csv already exists, do you want to scrape again? (y/n)")
    if input() == "y":
        os.remove(cwd+"/news_spider/"+company_name+".csv")
        print('Removed old csv file')
    else:
        print('Press enter to exit')
        delay = input()
        exit(0)
else:
    pass

scraping_command = "scrapy crawl"

if company_name in ['ILFS','IL&FS', 'ilfs', 'il&fs', 'infrastructure leasing and finance services']:
    command = scraping_command + " economictimes -o "+company_name+".csv"

    process = subprocess.Popen(command, shell=False, cwd=cwd + "\\news_spider")
    print(process)
else:
    print("company not found")

time.sleep(10)
print('\ncsv file saved in /news_spider/\nPress any button to exit.')
delay = input()