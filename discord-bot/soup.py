from bs4 import BeautifulSoup
import requests
import urllib.request
from urllib.parse import *

# make the sentence user insert url safe
textToSearch = "overjoyed cover"
query = urllib.parse.quote(textToSearch)

# google search using google dork site:youtube.com
url = "https://www.google.com/search?q=site%3Ayoutube.com+=" + query
response = requests.get(url, headers={
     'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'})
soup = BeautifulSoup(response.text, "lxml")

# search results
results = soup.findAll(attrs={'class': 'yuRUbf'})

# add search result into list of songs
i = 0
for div in results:
    for link in div.find_all('a'):
        if i >= 5:
            break

        if link['href'].startswith('https://www.youtube.com'):
            print(link['href'])
            i+=1
