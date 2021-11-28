# -*- coding: utf-8 -*-
"""
Created on Sun Nov 21 17:41:45 2021

@author: safiur
"""
import re
import sys
import time
import os.path
import webbrowser
import geoip2.database

countryAndMostviewDic = {}
countryAndMostViewedPageDic = {}
USStatesAndMostviewDic = {}
USStatesAndMostViewedPageDic = {}

def checkToIgnoreRequest(strToCheck):
    # Ignore all requests for images, CSS, and JavaScript
    # Also ignore all paths ending in .rss or .atom
    regexList = ['/[a-f0-9]+/css/','/[a-f0-9]+/images/','/[a-f0-9]+/js/',
             '/entry-images/','/images/','/user-images/','/static/',
             '/robots.txt','.*\.rss$','.*\.atom$']
    ignore = False
    for reg in regexList:
        if re.match(reg, strToCheck):
            ignore = True
            break
    return ignore

def updateMostViewedPageDic(originalDic):
    # Updating the most viewed page dictionary
    tempDic = originalDic
    finalDic = {}
    try:
        for currkey, currVal in originalDic.items():
            updatedKey = currkey.split('__ADDED__')[1]
            thePath = currkey.split('__ADDED__')[0]
            updatedVal = thePath + '__TOTAL#VIEW__' + str(currVal) # using _css_ since we know the path can not have "css" 
            for k,v in tempDic.items():
                if updatedKey == k.split('__ADDED__')[1]:
                    if v > currVal:
                        thePath = k.split('__ADDED__')[0]
                        updatedVal = thePath + '__TOTAL#VIEW__' + str(v)
            if updatedKey in finalDic:
                previousCount = int(finalDic[updatedKey].split('__TOTAL#VIEW__')[1])
                newCount = int(updatedVal.split('__TOTAL#VIEW__')[1])
                if newCount > previousCount:
                    finalDic[updatedKey] = updatedVal
            else:
                finalDic[updatedKey] = updatedVal
        originalDic = finalDic
    except Exception as ex:
        print(f'EXCEPTION: from updateMostViewedPageDic : {ex}')
    else:
        return finalDic
   
def showOutput():
    # Showing output to a html file
    outFileName = 'summary.html'
    Title = 'MaxMind :: GeoLite2 City database summary'
    HeaderCountry = 'Most Viewed Country:'
    HeaderStates = 'Most Viewed US States:'
    recordsToRetrieve = 10
    outputFile = open(outFileName, 'w')
    
    #generating country summary
    bodyOfCountry = 'Country :: #Most View :: The page (#viewCount)<br>'
    bodyOfCountry += "===================================<br>"
    countryItems = countryAndMostviewDic.items() # get a list of (key, value)
    for country, numberOfView in sorted(countryItems, key=lambda x: x[1], reverse = True)[:recordsToRetrieve]:
        thePage = countryAndMostViewedPageDic[country].split('__TOTAL#VIEW__')[0] \
        + ' (' + countryAndMostViewedPageDic[country].split('__TOTAL#VIEW__')[1] + ')' 
        bodyOfCountry += country + ' :: ' + str(numberOfView) + ' :: ' + thePage + '<br>'
    
    #generating US states summary 
    bodyOfStates = 'States :: #Most View :: The page (#viewCount)<br>'
    bodyOfStates += "==================================<br>"
    statesItems = USStatesAndMostviewDic.items() # get a list of (key, value)
    for states, numOfView in sorted(statesItems, key=lambda x: x[1], reverse = True)[:recordsToRetrieve]:
        thePage = USStatesAndMostViewedPageDic[states].split('__TOTAL#VIEW__')[0] \
        + ' (' + USStatesAndMostViewedPageDic[states].split('__TOTAL#VIEW__')[1] + ')'
        bodyOfStates += states + ' :: ' + str(numOfView) + ' :: ' + thePage + '<br>'
    #write to html
    outputFile.write(f"""<html>
    <head>
    <title>{Title}</title>
    </head>
    <body>
    <h2>{HeaderCountry}</h2>
    <p>{bodyOfCountry}</p><br>
    <h2>{HeaderStates}</h2>
    <p>{bodyOfStates}</p>
    </body>
    </html>""")
    outputFile.close()
    webbrowser.open(outFileName) #open in browser

def accessDB(dbFile, ipAddress, requestPath):
    # Retrieve the model class for the database for a given IP address
    # Updating the corresponding dictionaries
    success = False
    try:
        with geoip2.database.Reader(dbFile) as reader:
            try:
                response = reader.city(ipAddress);
                try:
                    global countryAndMostviewDic
                    global USStatesAndMostviewDic
                    global countryAndMostViewedPageDic
                    global USStatesAndMostViewedPageDic
                    countryName = response.country.name
                    #print(f'===================: {requestPath}\n{countryName}')
                    countryAndMostviewDic[countryName] = countryAndMostviewDic.get(countryName, 0) + 1
                    countryKey = requestPath + '__ADDED__' + countryName
                    if requestPath != '/':
                        countryAndMostViewedPageDic[countryKey] = countryAndMostViewedPageDic.get(countryKey, 0) + 1
                    try:
                        statesName = response.subdivisions.most_specific.name
                        if requestPath != '/' and countryName == 'United States' and not isinstance(statesName, type(None)):
                            USStatesAndMostviewDic[statesName] = USStatesAndMostviewDic.get(statesName, 0) + 1
                            stateKey = requestPath + '__ADDED__' + statesName
                            USStatesAndMostViewedPageDic[stateKey] = USStatesAndMostViewedPageDic.get(stateKey, 0) + 1
                    except Exception as ex:
                        print(f'IP address and corresponding country name exists, problem occured fetching states info: {ex}')
                except Exception as ex:
                        print(f'IP address exists, problem occured fetching country info: {ex}, moving to next record ...')
            except ValueError:
                print(f'Please check the ip address: {ipAddress}, is it IPv4/IPv6? Moving to next record ...')
            except Exception as ex:
                print(f'EXCEPTION: {ex} Moving to next record ...')
            else:
                success = True
    except Exception as ex:
        print(f'EXCEPTION: from accessDB func : {ex}')
    return success

def main(dbFile):
    try:
        global countryAndMostViewedPageDic
        global USStatesAndMostViewedPageDic
        with open('access.log') as file:
            count = 0
            for line in file:
                splittedLine = line.split()
                ipAddress = splittedLine[0]
                requestPath = splittedLine[6]
                ignoreRequest = checkToIgnoreRequest(requestPath)
                if not ignoreRequest:
                    success = accessDB(dbFile, ipAddress, requestPath)
                    if success:
                        count += 1
        countryAndMostViewedPageDic = updateMostViewedPageDic(countryAndMostViewedPageDic)
        USStatesAndMostViewedPageDic = updateMostViewedPageDic(USStatesAndMostViewedPageDic)
        showOutput()
        print(f'Total valid IP processed: {count}')
    except FileNotFoundError:
        print('Please check whether the current directory has the "access.log" file')
    except Exception as ex:
        print(f'EXCEPTION: from main func : {ex}')

if __name__ == '__main__':
    if( len(sys.argv) == 2):
        try:
            dbFile = sys.argv[1]
            if os.path.exists(dbFile):
                start = time.time()
                main(dbFile)
                end =  time.time()
                print(f'Total execution time: {end-start:.2f} seconds.')
            else:
                print('Please check the dbfile name (GeoLite2-City.mmdb) or if the current directory has the file?')
        except Exception as ex:
            print(f'EXCEPTION: from __main__ : {ex}')
    else:
        print('Please provide ONLY the database filename (GeoLite2-City.mmdb) as first argument.')