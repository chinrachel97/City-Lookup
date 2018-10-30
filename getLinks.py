from bs4 import BeautifulSoup
import requests
import csv

# get the main page content
url = 'http://www.city-data.com/'
response = requests.get(url)
html = response.content
soup = BeautifulSoup(html, "lxml")

# collect the links for states
statesElements = soup.findAll('a', attrs={'class': 'cities_list'})
statesLinks = []

for a in statesElements:
    if a['href'] not in statesLinks:
        statesLinks.append(a['href'])

# get the links for every city in each state
citiesLinks = []

for link in statesLinks:
    response = requests.get(link)
    html = response.content
    soup = BeautifulSoup(html, "lxml")
    citiesElements = soup.select("tr td b a")
    
    for a in citiesElements:
        citiesLinks.append(a['href'])

# write the links to a csv file
with open('cities.csv', 'a', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for link in citiesLinks:
        writer.writerow([link])
        print(link)