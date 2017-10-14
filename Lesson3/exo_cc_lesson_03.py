from urllib.request import urlopen
from multiprocessing import Pool
from bs4 import BeautifulSoup
import urllib.request, json
import pandas as pd
import numpy as np
import lxml.html
import requests
import getpass
import math
import re


URL='http://www.journaldunet.com/management/ville/classement/villes/population'
r = requests.get(URL)
soup = BeautifulSoup(r.text, 'html.parser')
cities = soup.tbody.find_all('a', href=re.compile('^/management/ville/'))
cities_cleaned = [c.text.split(' ', 1)[0] for c in cities]

cities_cleaned = cities_cleaned[:10]
cities_cleaned


def get_distance(cityA, cityB):
    data = requests.get("https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins="+cityA+"&destinations="+cityB+"&key=AIzaSyBKED6FYbqdBZvufn-cYD--4MpyClWFrh4").json()
    return data["rows"][0]["elements"][0]["distance"]["text"]

list_cities = []
for v in cities_cleaned:
    for v2 in cities_cleaned:
        list_cities.append(get_distance(v,v2))

matrix_cities = np.asarray(list_cities)
matrix_cities = matrix_cities.reshape(len(cities_cleaned), len(cities_cleaned))


df = pd.DataFrame(matrix_cities)
df.columns = cities_cleaned
df["Villes"] = cities_cleaned
df.set_index("Villes")
print(df)
