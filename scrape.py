from bs4 import BeautifulSoup
from random import randint
import requests
import time
import csv
import os
import re

# strip a string of its units
def clean(s):
    toRemove = [',', '$', ' ', '%']
    cleaned = ""
    for c in s:
        if c not in toRemove and not c.isalpha():
            cleaned += c
    return cleaned  

# get city + state name
def getCityStateName(soup, row):
    cityStateTag = soup.find('h1', attrs={'class': 'city'})
    children = cityStateTag.select('span')
    fullName = children[0].text.strip()
    r = "(\\w+), (\\w+)"
    m = re.search(r, fullName)
    stateName = m.group(2) 
    cityName = m.group(1)
    row.append(stateName)
    row.append(cityName)
    print("State:", stateName)
    print("City:", cityName)

# get population
def getPopulation(soup, row):
    cityPopulationTag = soup.find('section', attrs={'id': 'city-population'})
    child = cityPopulationTag.find('b', recursive=False)
    population = child.nextSibling.strip()
    row.append(clean(population))
    print("Population:", population)

# get population density + category
def getPopDensCat(soup, row):
    cityDensityTag = soup.find('section', attrs={'id': 'population-density'})
    children = cityDensityTag.select("p b")
    populationDensity = None
    for child in children:
        if child.text == "Population density:":
            populationDensity = child.nextSibling.strip()
    row.append(clean(populationDensity))
    print("Population Density: " + populationDensity + " people per square mile")

    populationDensityDeets = soup.find('span', attrs={'class': 'population-density'}).nextSibling
    r = "\\s*(?<=\\().+(?=\\))"
    densityDeets = re.search(r, populationDensityDeets).group(0).strip()
    row.append(densityDeets)
    print("Population Category: " + densityDeets)

# get median resident age
def getResAge(soup, row):
    ageTag = soup.find('section', attrs={'id': 'median-age'})
    children = ageTag.select("div table tr td")[1].select("img")
    medianResidentAge = children[0].nextSibling.strip()
    row.append(clean(medianResidentAge))
    print("Median Resident Age:", medianResidentAge)

# get estimated median household income
def getIncome(soup, row):
    incomeTag = soup.find('section', attrs={'id': 'median-income'})
    children = incomeTag.select("b")
    medianIncome = children[0].nextSibling
    r = "\\$(.*)\\s\\("
    medianIncome = re.search(r, medianIncome).group(1)
    row.append(clean(medianIncome))
    print("Median Household Income:", medianIncome)

# get unemployment percentage
def getUnemployment(soup, row):
    unemploymentTag = soup.find('section', attrs={'id': 'unemployment'})
    children = unemploymentTag.select("div table tr td")[1].select("p")
    unemployment = children[0].nextSibling.strip()
    row.append(clean(unemployment))
    print("Unemployment Percentage:", unemployment)

# get median rent
def getRent(soup, row):
    rentTag = soup.find('section', attrs={'id': 'median-rent'})
    children = rentTag.select("p b")
    rent = children[0].nextSibling.strip()
    row.append(clean(rent))
    print("Median Rent:", rent)

# get cost of living index + category
def getCOL(soup, row):
    costOfLivingTag = soup.find('section', attrs={'id': 'cost-of-living-index'})
    children = costOfLivingTag.select("b")
    costOfLiving = children[0].nextSibling.strip()
    row.append(costOfLiving)
    print("Cost of Living Index:", costOfLiving)

    COLCategory = children[1].text
    r = "(\\()(.*),.*"
    COLCategory = re.search(r, COLCategory).group(2)
    row.append(COLCategory)
    print("Cost of Living Category:", COLCategory)

# get median travel time to work
def getTravelTime(soup, row):
    travelTimeTag = soup.find('section', attrs={'id': 'education-info'})
    children = travelTimeTag.select("ul li")[4].select("b")
    travelTime = children[0].nextSibling.strip()
    row.append(clean(travelTime))
    print("Travel Time to Work:", travelTime)

# get crime index, U.S. average = 280.5
def getCrimeIdx(soup, row):
    crimeTag = soup.find('section', attrs={'id': 'crime'})
    children = crimeTag.select("div table tr td")
    crimeIndex = children[len(children)-1].text.strip()
    row.append(crimeIndex)
    print("Crime Index:", crimeIndex)

# get average household size
def getHhSize(soup, row):
    hSizeTag = soup.find('section', attrs={'id': 'households-stats'})
    children = hSizeTag.select("div div table tr td")[1].select("img")
    hSize = children[0].nextSibling.strip()
    row.append(clean(hSize))
    print("Average Household Size:", hSize)

# get air quality index, U.S. average = 91.1
def getAirQuality(soup, row):
    airQualityTag = soup.find('div', attrs={'id': 'air-pollution-chart'})
    children = airQualityTag.select("div div div table tr td")[1].select("p")
    airQualityIndex = children[0].nextSibling.strip()
    row.append(airQualityIndex)
    print("Air Quality Index:", airQualityIndex)

# get poverty percentage
def getPoverty(soup, row):
    povertyTag = soup.find('section', attrs={'id': 'poverty-level'})
    children = povertyTag.select("b")
    poverty = children[0].nextSibling.strip()
    row.append(clean(poverty))
    print("Poverty Percentage", poverty)

# get education gini index (inequality in education)
def getEduIneq(soup, row):
    giniTag = soup.find('section', attrs={'id': 'education-graphs'})
    children = giniTag.select("div div table tr td")[1].select("p")
    gini = children[0].nextSibling.strip()
    row.append(gini)
    print("Inequality in Education Index:", gini)

# csv header
header = ["State",                  # State
    "City",                         # City
    "POP",                          # Population 
    "POP Density (people/sqmile)",  # Population Density 
    "POP Category",                 # Population Category
    "Med. Res. Age (yrs)",          # Median Resident Age
    "Med. HH Income ($)",           # Median Household Income
    "Unemployment %",               # Unemployment Percentage
    "Med. Rent ($)",                # Median Rent
    "COL Idx",                      # Cost of Living Index
    "COL Category",                 # Cost of Living Category
    "Mean Commute (mins)",          # Travel Time to Work
    "Crime Idx",                    # Crime Index
    "Avg. HH Size (person)",        # Average Household Size
    "Air Quality Idx",              # Air Quality Index
    "Poverty %",                    # Poverty Percentage
    "Edu. Ineq. Idx"                # Education Inequality Index
]

# init the csv file
filename = "city-data-scrape.csv"
with open(filename, 'a', newline='') as csvfile:
    if os.stat(filename).st_size == 0:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(header)

# get all the city links
cityLinks = []
with open('cities.csv', 'r', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        cityLinks.append(row)

# go through a certain range of cities
for i in range(10):
    # array to hold all the data for a city
    row = []

    # get the city to scrape
    #response = requests.get('http://127.0.0.1/CSCE470/Anchorage-Alaksa.html')
    response = requests.get(' http://www.city-data.com/city/' + cityLinks[i][0])
    html = response.content
    soup = BeautifulSoup(html, "lxml")

    # start timing
    startTime = time.time()
        
    # get city + state name
    try:
        getCityStateName(soup, row)
    except:
        row.append("")
    
    # get population
    try:
        getPopulation(soup, row)
    except:
        row.append("")
    
    # get population density + category
    try:
        getPopDensCat(soup, row)
    except:
        row.append("")
    
    # get median resident age
    try:
        getResAge(soup, row)
    except:
        row.append("")

    # get estimated median household income
    try:
        getIncome(soup, row)
    except:
        row.append("")

    # get unemployment percentage
    try:
        getUnemployment(soup, row)
    except:
        row.append("")

    # get median rent
    try:
        getRent(soup, row)
    except:
        row.append("")

    # get cost of living index + category
    try: 
        getCOL(soup, row)
    except:
        row.append("")

    # get median travel time to work
    try:
        getTravelTime(soup, row)
    except:
        row.append("")

    # get crime index, U.S. average = 280.5
    try: 
        getCrimeIdx(soup, row)
    except:
        row.append("")

    # get average household size
    try:
        getHhSize(soup, row)
    except:
        row.append("")

    # get air quality index, U.S. average = 91.1
    try:
        getAirQuality(soup, row)
    except:
        row.append("")

    # get poverty percentage
    try:
        getPoverty(soup, row)
    except:
        row.append("")

    # get education gini index (inequality in education)
    try: 
        getEduIneq(soup, row)
    except:
        row.append("")

    # end timing
    elapsedTime = time.time() - startTime
    print("Time taken:", elapsedTime)

    # write data to csv file
    with open('city-data-scrape.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(row)

    time.sleep(randint(1, 4))