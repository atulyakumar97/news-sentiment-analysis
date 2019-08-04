# News Sentiment Analysis

The program crawls [moneycontrol](https://www.moneycontrol.com/) and [economictimes](https://economictimes.indiatimes.com/) to fetch data of companies listed in the input.xlsx file. Once the data is scraped and a csv file is built, relative analysis is done using analyse.py to classify the companies into RED, AMBER and GREEN. Absolute scoring is done using the score.py script.

The [master branch](https://github.com/atulyakumar97/news-sentiment-analysis/tree/master) contains the source code for the application.<br>
[dist-windows](https://github.com/atulyakumar97/news-sentiment-analysis/tree/dist-windows) branch contains the exe files and support files independant of the python installation.<br>

### Setup:

1. Click <b>Clone or Download</b> and then <b>Download ZIP</b> button to download the application.
2. Extract all files to a folder and run the applications as specified below.

### How to run:

1. Make changes to input.xlsx (Configuration settings given below)
2. Run News Scraper.exe
3. Output is stored in Scrape Output.csv
4. Run Score Generator.exe and Scrape Analyser.exe for analysing scraped content.
5. Output is stored in Score Output.xlsx and Analyse Output.xlsx respectively

![icons](https://raw.githubusercontent.com/atulyakumar97/news-sentiment-analysis/master/.images/icons.PNG)

| Application        | input.xlsx columns | Output File         |
|--------------------|:------------------:| -------------------|
|   News Scraper.exe |        A to F      |  Scrape Output.csv  |
| Score Generator.exe|        H to L      |  Score Output.xlsx  |
| Scrape Analyser.exe|        I to L      | Analyse Output.xlsx |

### input.xlsx

![news scraper input](https://raw.githubusercontent.com/atulyakumar97/news-sentiment-analysis/master/.images/input-scraper.PNG)

|     Parameter    |        Ideal Value        |                              Description                                                   |
| -----------------|---------------------------| :------------------------------------------------------------------------------------------|
| COMPANYNAME      | String, exact match       | Enter company names as close to the company name listed on the stocks page of Economic Times and Money Control. |
| THRESHOLD        | 0.75 to 0.85              | This is the percentage match between input company names and website listed company names. |
| DATEFROM         | DD-MM-YYYY                | Data from this period will be scraped |
| DATETO           | DD-MM-YYYY	               | Data till this period will be scraped  |
| WEBSITE          | Select at least one site	 | Moneycontrol or Economictimes  |
| ROTATING_PROXIES | 0 to 100<br>0 = No proxy  | Used to bypass bans while scraping. Increasing proxy number might lead to slower data Scraping. |

![score generator, scrape analyser](https://raw.githubusercontent.com/atulyakumar97/news-sentiment-analysis/master/.images/input-analyser.PNG)

|     Parameter     |               Ideal Value        | Description  |
| ------------------|----------------------------------| :-------------------------------------------------------------------------------|
| POSITIVE_KEYWORDS | String                           | Positive Keywords list|
| NEGATIVE_KEYWORDS | String                           | Negative Keywords list |
| SEARCH OPTION     | Article Title or Article Content | Select which content you want the program to analyse |
| N_STDDEV_RED      | Float (0.5, 1, 1.5, 2)           | If keyword count greater than mean + (N_STDDEV_RED * stddev) then the company is labelled RED|
| N_STDDEV_AMBER    | Float (0.5, 1, 1.5, 2)	      | If keyword count greater than mean + (N_STDDEV_AMBER * stddev) then the company is labelled AMBER |

### License and Copyright

Licensed under the [MIT License](license.txt)
	
