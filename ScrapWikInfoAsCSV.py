import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from urllib.request import urlopen
#ScrappingTest is the csv in which you will store the list of wiki searches
# I am searching for two companies, Will attach sample csv
temp = pd.read_csv('scrapingTest.csv')
import time
start_time = time.time()


res = []
count=1
for i in temp['Company Name']:
    i=str(i).split('-')[0].strip()
    company_name = i
    try:
        company_name = company_name.replace(' ', '_')
        baseurl = 'https://en.wikipedia.org/wiki/'
        url = baseurl + company_name
        html = urlopen(url)
        soup = BeautifulSoup(html, 'html.parser')
        tableclass = "infobox vcard"
        result = soup.find('table', attrs={'class': tableclass})

        df = pd.read_html(str(result))

    # Create array to hold the data we extract
        info = []

        for table in result:
            rows = table.find_all('tr')

            for row in rows:
                cells = row.find_all('td')
                if (len(cells) < 1):
                    info.append("NULL")
                    continue

                rank = cells[0]
                info.append(rank.text.strip())

    # Create array to hold the data we extract
        subject = []

        for table in result:
            rows = table.find_all('tr')

            for row in rows:
                cells = row.find_all('th')

                if (len(cells) < 1):
                    subject.append("NULL")
                    continue
                rank = cells[0]
                subject.append(rank.text.strip())
        d = {'subject': subject, 'info': info}
        df = pd.DataFrame(d)
        res.append(df)
    except:
        res.append("NULL")
        continue
    print("Working on ",count," Row ")
    count=count+1

#printing the 1st result of the file you can use the for loop to get output for all the searches
print(res[0])
print("Exporting the result of first company:")
res[0].to_csv("FirstComapny.csv")
print("--- %s seconds ---" % (time.time() - start_time))
