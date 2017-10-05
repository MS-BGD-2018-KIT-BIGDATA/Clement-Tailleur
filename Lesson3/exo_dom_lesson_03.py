from urllib.request import urlopen
from multiprocessing import Pool
from bs4 import BeautifulSoup
import urllib.request, json
import pandas as pd
import lxml.html
import requests
import getpass
import math
import re

username = input('Github username: ')
password = getpass.getpass('Github password: ')

URL = "https://gist.github.com/paulmillr/2657075"

r = requests.get(URL)
soup = BeautifulSoup(r.text, 'html.parser')
users = soup.tbody.find_all('a', href=re.compile('^https://github.com/'))
users_cleaned = [u.text for u in users]

Dict_Github = {'Rank': list(range(1, 257)),
               'Username': users_cleaned}

df = pd.DataFrame(Dict_Github)
df = df.set_index('Rank')

def get_github_level(username):
    p, stars_number, projects_number = 1, 0, 0
    data = requests.get("https://api.github.com/users/" + username + "/repos?page=1&per_page=100", auth=(username, password)).json()
    while(len(data) != 0):
        projects_number += len(data)
        for i in range(len(data)):
            stars_number += data[i]["stargazers_count"]
        p += 1
        data = requests.get("https://api.github.com/users/" + username + "/repos?page=" + str(p) + "&per_page=100", auth=(username, password)).json()
    if projects_number == 0:
        return 0
    return round(stars_number/projects_number, 2)

p = Pool(3)
fraicheur_github = p.map(get_github_level, users_cleaned)
df["Star"] = fraicheur_github
df_sorted = df.sort_values(by="Star", ascending=False).copy()
df_sorted.head()
