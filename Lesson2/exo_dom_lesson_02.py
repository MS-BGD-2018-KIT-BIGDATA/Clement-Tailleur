from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import lxml.html
import requests
import sys

def french_finance_scraper_1(year):
    year = str(year)
    URL = "http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=" + year
    page = urlopen(URL).read()
    html = lxml.html.fromstring(page)
    scraping = html.xpath("//td[@class='montantpetit G']")

    data_list = [sc.text_content() for sc in scraping]
    data_list = data_list[:6] + data_list[9:15]
    dates_list_cleaned = [dlc.replace('\xa0','').strip() for dlc in data_list]

    data = {"Valeurs": ['Euros par habitant', 'Moyenne de la strate']}
    i=0
    for c in ['A_' + year, 'B_' + year, 'C_' + year, 'D_' + year]:
        data[c] = dates_list_cleaned[i+1:i+3]
        i += 3

    return pd.DataFrame(data).set_index(['Valeurs'])


def french_finance_scraper_2(year):
    year = str(year)
    URL = "http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=" + year
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, 'html.parser')
    scraping = soup.find_all('td',attrs={"class": u"montantpetit G"})

    data_list = []
    for dl in scraping:
        data_list.append(dl.text.replace('\xa0','').strip())
    dates_list_cleaned = data_list[:6] + data_list[9:15]

    data = {"Valeurs": ['Euros par habitant', 'Moyenne de la strate']}
    i=0
    for c in ['A_' + year, 'B_' + year, 'C_' + year, 'D_' + year]:
        data[c] = dates_list_cleaned[i+1:i+3]
        i += 3

    return pd.DataFrame(data).set_index(['Valeurs'])


for year_studied in range(2010, 2016):
    print(french_finance_scraper_1(year_studied))
    print()

print()
for year_studied in range(2010, 2016):
    print("Data frame function 1 equals Data frame function 2 in %d:" % year_studied)
    print(french_finance_scraper_1(year_studied).equals(french_finance_scraper_2(year_studied)))
