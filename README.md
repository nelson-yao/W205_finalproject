# W205_finalproject

##Summary
To finish the project, I scraped data from www.comicchron.com, used the results as request terms for Marvel API, then extracted meaningful results from information returned from API calls. This process can be time-consuming. The scraping covers 18 years of comic book sales (1997 to 2015). Over 9000 comic books were used as search terms for marvel API. All of these can be time consuming. Another problem is that Marvel API only allows 3000 calls per key. When I did the project, I did the collection process over several days. So to better demonstrate the process, I made scripts that would build a mini version of the project. These scripts are included in the "Test" folder

The contents of the folders are as the following:

original: the code used to finish the project originally
test: the code used to build a minimized version of the project.
comic: the code used to scrape data from the website

In addition, the file "Dependencies" include a list of the dependency package for python. Note the scrapy package on works on Python 2.7. This package can be tricky to install. Please refer to the [scrapy installation guide](http://doc.scrapy.org/en/latest/intro/install.html) for help if you have trouble.

There is also a screenshot of the scraping process in the main folder.

## Code Testing
You can use the contents of the "Test" folder to build a mini version of the project.

### Scraping
Enter the scraping folder:
```
cd comic
```

There are three spiders, "salestable" scrape the sales data from 1997 to 2011, "salestable" scrape the data from 2012 to 2015. Two spiders were used because the webpage structures were slightly different for those before and after 2012. "salestabletest" is the third spider that scrape Marvel comic sales from October and November 2011, and is used for testing purposes.

To start scraping using the test spider, from "comic" folder:
```
scrapy crawl salestabletest -o scraping_result_test.json
```
This saves the results to scraping_result_test.json.

### API requests and extraction
First, go to the ```Test``` folder.

```getMarvel_test.py``` uses information retreived from scraping to request comic book character appearances from Marvel. It needs to be supplied an argument that is the name of the file of the scraping results.
To run the API requests:
```
python getMarvel_test.py scraping_result_test.json
```
The script generates a file "responses_test.json" that contains all information retrieved from Marvel API, stored in JSON  format.

To extract character appearences, roles (heroic or villainous), full book titles, and other information from the objects returned Marvel API, use "DataExtract_test.py":
```
python DataExtract_test.py responses_test.json
```
The extraction script produces two csv files, ```marvelchar_test.csv``` and ```marveledges_test.csv```. The first contains the characters extracted from the API responses, their role, the book title they appeared in and the number of orders. "marveledges_test.csv" explore the connection between characters. It contains every possible pairs of characters that appear together in a comic book.

### Building database


To build the data base, first generate two sql files that do the data insertion. This is done by using ```csvtosql.py```, which needs two arguments:
```
python csvtosql.py marvelchar_test.csv marveledges_test.csv
```
This script generates ```char_sql_test.sql``` and ```edge_sql_test.sql```, which put data into the data table ```marvelchar_test``` and ```marveledges_test```, respectively.


Assuming postgres is installed, log into postgres using:
```
psql -U postgres
```
To put the database together, run the following command inside postgres:
```
\i database_test.sql
```
To query results from the data base, one can use ```testquery.py```. When supplied with different arguments, different query tasks can be performed. The arguments and their functions are as the following:

```python testquery.py totalsales Spider-Man```  returns the total orders of the comics that Spider-Man appeared in
```python testquery.py most_profitable_character``` returns the top 10 characters that have the most comic books sold
```python testquery.py most_sold_with Wolverine``` show the top 10 characters who appeared with Wolverine,  ranked by comic book sales

Note that not all spellings of the characters are recognized. For example, "spider man" will not return any query results.
Note that the intermediate files described above are all available in the ```Test``` folder. So the user can start at any of the steps

### Original Project
Under folder ``` original ```, there are scripts that correspond to the scripts described above in the ```Test``` folder.
```sales.json``` and ```sales2012.json``` contain the scraping results. ```responses2012_1```, ```responses2012_2```, and ```part(1 to 5)responses.txt``` include the response of Marvel APIs. The rest of the files are:

- DataExtract_original.py  :  extract character data from API responses, generates ```marvelheroesall.csv``` and ```marveledges.csv```
- csv2sql.py               : generates sql data insertion files, ```char_sql.sql``` and ```edge_sql.sql```
- database_full.sql        : builds the database, runs in the same way as the counterpart in ```Test```
- fullquery.py             : used to query results from the database, used in the same way as ```testquey.py```
- marvelquery.sql          : contains the query used to generate the data for the presentation

### Machine learning

I attempted to build a model that can predict comic booko sales based its character appearances, but it did not work out well. I tried suppor vector regression, linear regression and random forest, the best R2 scores I can get was 11%. See ```ML_train.py``` for details. This scrip requires sci-kit learn which can be installed using:
```
pip install -U scikit-learn
```
