# News Sentiment Analysis

The program crawls [moneycontrol](https://www.moneycontrol.com/) and [economictimes](https://economictimes.indiatimes.com/) to fetch data of companies listed in the input.xlsx file. Once the data is scraped and a csv file is built, relative analysis is done using analyse.py to classify the companies into RED, AMBER and GREEN. Absolute scoring is done using the score.py script.

The [master branch](https://github.com/atulyakumar97/news-sentiment-analysis/tree/master) contains the source code for the application.<br>
[dist-windows](https://github.com/atulyakumar97/news-sentiment-analysis/tree/dist-windows) branch contains the exe files and support files independant of the python installation.<br>

### Installation

To run scrape.py, analyse.py or score.py first install all dependencies by: 

```
pip install -r requirements.txt
```

| Script    | input.xlsx columns | Output File         |
|-----------|:------------------:| -------------------|
| scrape.py |        A to F      |  Scrape Output.csv  |
| score.py  |        H to L      |  Score Output.xlsx  |
| analyse.py|        I to L      | Analyse Output.xlsx |

### input.xlsx configuration

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

Licensed under the [MIT License](LICENSE)
