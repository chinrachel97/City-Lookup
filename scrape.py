from bs4 import BeautifulSoup
import requests
import time
import csv
import os
import re

'''
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
'''        

# init the csv rows
header = ["State",
    "City",
    "Population",
    "Population Density",
    "Population Category",
    "Median Resident Age",
    "Median Household Income",
    "Unemployment Percentage",
    "Median Rent",
    "Cost of Living Index",
    "Cost of Living Category",
    "Travel Time to Work",
    "Crime Index",
    "Avg. Household Size",
    "Air Quality Index",
    "Poverty Percentage",
    "Education Inequality Index"
]
toSave = []

# init the csv file
filename = "city-data-scrape.csv"

with open(filename, 'a', newline='') as csvfile:
    if os.stat(filename).st_size == 0:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(header)

# get a specific city
#anchorageLink = citiesLinks[0]
#response = requests.get(' http://www.city-data.com/city/' + anchorageLink)
response = requests.get('http://127.0.0.1/CSCE470/Anchorage-Alaksa.html')
html = response.content
soup = BeautifulSoup(html, "lxml")

# start timing
startTime = time.time()

# get city + state name
cityStateTag = soup.find('h1', attrs={'class': 'city'})
children = cityStateTag.select('span')
fullName = children[0].text.strip()
r = "(\\w+), (\\w+)"
m = re.search(r, fullName)
stateName = m.group(2) 
cityName = m.group(1)
toSave.append(stateName)
toSave.append(cityName)
print("State:", stateName)
print("City:", cityName)

# get population
cityPopulationTag = soup.find('section', attrs={'id': 'city-population'})
child = cityPopulationTag.find('b', recursive=False)
population = child.nextSibling.strip()
toSave.append(population)
print("Population:", population)

# get population density + category
cityDensityTag = soup.find('section', attrs={'id': 'population-density'})
children = cityDensityTag.select("p b")
populationDensity = None
for child in children:
    if child.text == "Population density:":
        populationDensity = child.nextSibling.strip()
toSave.append(populationDensity)
print("Population Density: " + populationDensity + " people per square mile")

populationDensityDeets = soup.find('span', attrs={'class': 'population-density'}).nextSibling
r = "\\s*(?<=\\().+(?=\\))"
densityDeets = re.search(r, populationDensityDeets).group(0).strip()
toSave.append(densityDeets)
print("Population Category: " + densityDeets)

# get median resident age
ageTag = soup.find('section', attrs={'id': 'median-age'})
children = ageTag.select("div table tr td")[1].select("img")
medianResidentAge = children[0].nextSibling.strip()
toSave.append(medianResidentAge)
print("Median Resident Age:", medianResidentAge)

# get estimated median household income
incomeTag = soup.find('section', attrs={'id': 'median-income'})
children = incomeTag.select("b")
medianIncome = children[0].nextSibling
r = "\\$(.*)\\s\\("
medianIncome = re.search(r, medianIncome).group(1)
toSave.append(medianIncome)
print("Median Household Income:", medianIncome)

# get unemployment percentage
unemploymentTag = soup.find('section', attrs={'id': 'unemployment'})
children = unemploymentTag.select("div table tr td")[1].select("p")
unemployment = children[0].nextSibling.strip()
toSave.append(unemployment)
print("Unemployment Percentage:", unemployment)

# get median rent
rentTag = soup.find('section', attrs={'id': 'median-rent'})
children = rentTag.select("p b")
rent = children[0].nextSibling.strip()
toSave.append(rent)
print("Median Rent:", rent)

# get cost of living index + category
costOfLivingTag = soup.find('section', attrs={'id': 'cost-of-living-index'})
children = costOfLivingTag.select("b")
costOfLiving = children[0].nextSibling.strip()
toSave.append(costOfLiving)
print("Cost of Living Index:", costOfLiving)

COLCategory = children[1].text
toSave.append(COLCategory)
print("Cost of Living Category:", COLCategory)

# get median travel time to work
travelTimeTag = soup.find('section', attrs={'id': 'education-info'})
children = travelTimeTag.select("ul li")[4].select("b")
travelTime = children[0].nextSibling.strip()
toSave.append(travelTime)
print("Travel Time to Work:", travelTime)

# get crime index, U.S. average = 280.5
crimeTag = soup.find('section', attrs={'id': 'crime'})
children = crimeTag.select("div table tr td")
crimeIndex = children[len(children)-1].text.strip()
toSave.append(crimeIndex)
print("Crime Index:", crimeIndex)

# get average household size
hSizeTag = soup.find('section', attrs={'id': 'households-stats'})
children = hSizeTag.select("div div table tr td")[1].select("img")
hSize = children[0].nextSibling.strip()
toSave.append(hSize)
print("Average Household Size:", hSize)

# get median year house/condo built (SKIP; cannot find)

# get air quality index, U.S. average = 91.1
airQualityTag = soup.find('div', attrs={'id': 'air-pollution-chart'})
children = airQualityTag.select("div div div table tr td")[1].select("p")
airQualityIndex = children[0].nextSibling.strip()
toSave.append(airQualityIndex)
print("Air Quality Index:", airQualityIndex)

# get poverty percentage
povertyTag = soup.find('section', attrs={'id': 'poverty-level'})
children = povertyTag.select("b")
poverty = children[0].nextSibling.strip()
toSave.append(poverty)
print("Poverty Percentage", poverty)

# get education gini index (inequality in education)
giniTag = soup.find('section', attrs={'id': 'education-graphs'})
children = giniTag.select("div div table tr td")[1].select("p")
gini = children[0].nextSibling.strip()
toSave.append(gini)
print("Inequality in Education Index:", gini)

# end timing
elapsedTime = time.time() - startTime
print("Time taken:", elapsedTime)

# write data to csv file
with open('city-data-scrape.csv', 'a', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(toSave)
