#!/usr/bin/env python

# imports
import operator
import math
import csv
import sys

# calculate the dot product
def calcDotProd(vec1, vec2):
    if len(vec1) != len(vec2):
        return None
    dotProd = 0.0
    for i in range(len(vec1)):
        dotProd += vec1[i] * vec2[i]
    return dotProd

# calculate the magnitude
def calcMagnitude(vec):
    sum = 0.0
    for i in range(len(vec)):
        sum += vec[i] * vec[i]
    return math.sqrt(sum)

# calculate the average input city
def calcAvgQuery(listOfVecs):
    retVec = []
    vecSize = len(listOfVecs[0])

    # init the return vector
    for i in range(vecSize):
        retVec.append(0)

    # get the sum of all values at each index
    for vec in listOfVecs:
        for i in range(vecSize):
            retVec[i] += vec[i]

    # get the average
    for i in range(vecSize):
        retVec[i] /= vecSize

    return retVec

# calculate the cosine similarity
def cosine(query, compare):
    if calcMagnitude(query) == 0 or calcMagnitude(compare) == 0:
        return 0
    else:
        return calcDotProd(query, compare) / (calcMagnitude(query) * calcMagnitude(compare))

# return the top 10 results in a dictionary
def returnTop10(dict, inputs):
    sortedDict = sorted(dict.items(), key=operator.itemgetter(1), reverse=True)
    top10 = []

    for i in range(len(sortedDict)):
        # make sure the similar cities do not include user inputted cities
        if sortedDict[i][0] not in inputs:
            top10.append((sortedDict[i][0], sortedDict[i][1]))

        # quit if there are already 10 similar cities saved
        if len(top10) == 10:
            break

    return top10

filename = 'city-data-scrape.csv'       # the filename with all city data
userInput = ("Austin", "Texas")         # default user input
userVec = []                            # user's input vec with normalized values
cityDetails = {}                        # normalized values for each (city,state) pair
cosineScores = {}                       # cosine scores for each (city,state) pair
colIdx = {}                             # csv column names to index

# read and load data from the file
with open(filename, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')

    # init the colIdxs with the header
    idx = 0
    for item in reader.next():
        colIdx[item] = idx
        idx += 1

    # parse the data and get just the relevant data
    for row in reader:
        dkey = (row[1], row[0])
        cityDetails[dkey] = (float(row[colIdx["Norm POP"]]),
                                float(row[colIdx["Norm POP Density"]]),
                                float(row[colIdx["Norm Med. Res Age"]]),
                                float(row[colIdx["Norm Med. HH Income"]]),
                                float(row[colIdx["Norm Unemployment"]]),
                                float(row[colIdx["Norm Med. Rent"]]),
                                float(row[colIdx["Norm COL Idx"]]),
                                float(row[colIdx["Norm Mean Commute"]]),
                                float(row[colIdx["Norm Crime Idx"]]),
                                float(row[colIdx["Norm HH Size"]]),
                                float(row[colIdx["Norm Air Quality"]]),
                                float(row[colIdx["Norm Poverty"]]),
                                float(row[colIdx["Norm Edu Ineq"]]))

# parse the cmdline arguments
cmdArgs = []
cmdArgsDeets = []
for i in range(1, len(sys.argv)):
    parsedInput = sys.argv[i].split(",")
    city = parsedInput[0]
    state = parsedInput[1]

    # convert the (city,state) pairs to their vectors
    cmdArgs.append((city, state))
    cmdArgsDeets.append(cityDetails[(city, state)])

# get the average user input
if cmdArgsDeets > 1:
    userInput = ("avg", "avg")
userVec = calcAvgQuery(cmdArgsDeets)

# go through all cities in the dictionary
for key in cityDetails.keys():
    # skip the city if it is the same one
    if userInput == key:
        continue

    # calculate the cosine
    cosineScores[key] = cosine(userVec, cityDetails[key])

# get the top 10 most similar cities
top10Cities = returnTop10(cosineScores, cmdArgs)
for city in top10Cities:
    print(', '.join(city[0]))
