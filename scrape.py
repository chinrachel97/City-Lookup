from bs4 import BeautifulSoup
import requests
import csv

# get the main page content
url = 'http://www.city-data.com/'
response = requests.get(url)
html = response.content
soup = BeautifulSoup(html)

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
    soup = BeautifulSoup(html)
    citiesElements = soup.select("tr td b a")
    
    for a in citiesElements:
        citiesLinks.append(a['href'])
            
# get a specific city
anchorageLink = citiesLinks[0]
response = requests.get(' http://www.city-data.com/city/' + anchorageLink)
html = response.content
soup = BeautifulSoup(html)

# get the population number
cityPopulationTag = soup.find('section', attrs={'id': 'city-population'})
child = cityPopulationTag.find('b', recursive=False)
population = child.nextSibling
print(population)

# get the population density
cityDensityTag = soup.find('section', attrs={'id': 'population-density'})
children = cityDensityTag.select("p b")
populationDensity = None
for child in children:
    if child.text == "Population density:":
        populationDensity = child.nextSibling
populationDensityDeets = soup.find('span', attrs={'class': 'population-density'}).nextSibling
print(populationDensity + " people per square mile " + populationDensityDeets)

toSave = [population, populationDensity, populationDensityDeets]
with open('city-data-scrape.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(toSave)