# -*- coding: utf-8 -*-
"""
Created on Sat Nov 27 17:41:45 2021

@author: safiur
"""
import re
import sys
import time
import os.path
import webbrowser
import geoip2.database

accessLogFileName = 'access.log'
dbFileName = 'GeoLite2-City.mmdb'

countryAndMostviewDic = {}
countryAndMostViewedPageDic = {}

USStatesAndMostviewDic = {}
USStatesAndMostViewedPageDic = {}

unknownCountryList = {}
unknownStatesList = {}

def checkToIgnoreRequest(strToCheck):
    # Ignore all requests for images, CSS, and JavaScript
    # Also ignore all paths ending in .rss or .atom
    regexList = ['/[a-f0-9]+/css/','/[a-f0-9]*/images/','/[a-f0-9]+/js/',
             '/entry-images/','/images/','/user-images/','/static/',
             '/robots.txt','/favicon.ico','.*\.rss$','.*\.atom$']
    ignoreFlag = False
    for reg in regexList:
        if re.match(reg, strToCheck):
            ignoreFlag = True
            break
    return ignoreFlag

def updateMostViewedPageDic(originalDic):
    # Updating the most viewed page dictionary
    tempDic = originalDic
    finalDic = {}
    try:
        for currkey, currVal in originalDic.items():
            updatedKey = currkey.split('__ADDED__')[1]
            thePath = currkey.split('__ADDED__')[0]
            updatedVal = thePath + '__TOTAL#VIEW__' + str(currVal)
            if updatedKey not in finalDic:
                for k,v in tempDic.items():
                    if updatedKey == k.split('__ADDED__')[1]:
                        if v > currVal:
                            thePath = k.split('__ADDED__')[0]
                            updatedVal = thePath + '__TOTAL#VIEW__' + str(v)
                            currVal = v # updating most viewed page
                finalDic[updatedKey] = updatedVal
    except Exception as ex:
        print(f'EXCEPTION: from updateMostViewedPageDic function: {ex}')
    else:
        return finalDic
   
def showOutput():
    # Showing output to a html file
    try:
        outFileName = 'summary.html'
        Title = 'MaxMind :: GeoLite2 City database summary'
        HeaderCountry = 'Most Viewed Country:'
        HeaderStates = 'Most Viewed US States:'
        recordsToRetrieve = 10 if len(countryAndMostviewDic) >=10 else len(countryAndMostviewDic)
        outputFile = open(outFileName, 'w')
        
        #generating country summary
        bodyOfCountry = 'Country :: #Most View :: "The most viewed page" (#viewCount)<br>'
        consoleOutputCountry = 'Country :: #Most View :: "The most viewed page" (#viewCount)\n'
        bodyOfCountry += "===============================================<br>"
        consoleOutputCountry += "============================================================\n"
        countryItems = countryAndMostviewDic.items() # get a list of (key, value)
        for country, numberOfView in sorted(countryItems, key=lambda x: x[1], reverse = True)[:recordsToRetrieve]:
            mostViewedPage = '"' + countryAndMostViewedPageDic[country].split('__TOTAL#VIEW__')[0] \
            + '" (' + countryAndMostViewedPageDic[country].split('__TOTAL#VIEW__')[1] + ')' 
            bodyOfCountry += country + ' :: ' + str(numberOfView) + ' :: ' + mostViewedPage + '<br>'
            consoleOutputCountry += country + ' :: ' + str(numberOfView) + ' :: ' + mostViewedPage + '\n'
        
        #generating US states summary 
        bodyOfStates = 'States :: #Most View :: "The most viewed page" (#viewCount)<br>'
        consoleOutputStates = 'States :: #Most View :: "The most viewed page" (#viewCount)\n'
        bodyOfStates += "=============================================<br>"
        consoleOutputStates += "============================================================\n"
        statesItems = USStatesAndMostviewDic.items() # get a list of (key, value)
        for states, numOfView in sorted(statesItems, key=lambda x: x[1], reverse = True)[:recordsToRetrieve]:
            mostViewedPage = '"' + USStatesAndMostViewedPageDic[states].split('__TOTAL#VIEW__')[0] \
            + '" (' + USStatesAndMostViewedPageDic[states].split('__TOTAL#VIEW__')[1] + ')'
            bodyOfStates += states + ' :: ' + str(numOfView) + ' :: ' + mostViewedPage + '<br>'
            consoleOutputStates += states + ' :: ' + str(numOfView) + ' :: ' + mostViewedPage + '\n'
        #write to html
        print(f"{consoleOutputCountry}\n{consoleOutputStates}")
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
    except Exception as ex:
        print(f'EXCEPTION: from showOutput function : {ex}')

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
                    if not isinstance(countryName, type(None)):
                        countryAndMostviewDic[countryName] = countryAndMostviewDic.get(countryName, 0) + 1
                        countryKey = requestPath + '__ADDED__' + countryName
                        if requestPath != '/':
                            countryAndMostViewedPageDic[countryKey] = countryAndMostViewedPageDic.get(countryKey, 0) + 1
                        try:
                            statesName = response.subdivisions.most_specific.name
                            if not isinstance(statesName, type(None)):
                                if requestPath != '/' and countryName == 'United States':
                                    USStatesAndMostviewDic[statesName] = USStatesAndMostviewDic.get(statesName, 0) + 1
                                    stateKey = requestPath + '__ADDED__' + statesName
                                    USStatesAndMostViewedPageDic[stateKey] = USStatesAndMostViewedPageDic.get(stateKey, 0) + 1
                            else:
                                #print(f'Found Unknown State for, IP: {ipAddress}, Country: {countryName}, added to Unknown State list')
                                unknownStatesList[ipAddress] = 'unknown'
                        except Exception:
                            #print(f'Found Unknown State for, IP: {ipAddress}, Country: {countryName}, added to Unknown State list')
                            unknownStatesList[ipAddress] = 'unknown'
                    else:
                        #print(f'Found Unknown Country for, IP: {ipAddress}, added to Unknown Country list')
                        unknownCountryList[ipAddress] = 'unknown'
                except Exception:
                        #print(f'Found Unknown Country for, IP: {ipAddress}, added to Unknown Country list!')
                        unknownCountryList[ipAddress] = 'unknown'
            except ValueError:
                print(f'Please check the ip address: {ipAddress}, is it IPv4/IPv6? Moving to next record ...')
            except Exception as ex:
                print(f'EXCEPTION: {ex} Moving to next record ...')
            else:
                success = True
    except Exception as ex:
        print(f'EXCEPTION: from accessDB function : {ex}')
    return success

def main(accessLogFile, dbFileName):
    try:
        global countryAndMostViewedPageDic
        global USStatesAndMostViewedPageDic
        with open(accessLogFile) as file:
            count = 0
            for line in file:
                splittedLine = line.split()
                ipAddress = splittedLine[0]
                requestPath = splittedLine[6]
                ignoreRequest = checkToIgnoreRequest(requestPath)
                if not ignoreRequest:
                    success = accessDB(dbFileName, ipAddress, requestPath)
                    if success:
                        count += 1
        countryAndMostViewedPageDic = updateMostViewedPageDic(countryAndMostViewedPageDic)
        USStatesAndMostViewedPageDic = updateMostViewedPageDic(USStatesAndMostViewedPageDic)
        showOutput()
        print(f'Summary:\nTotal valid IP processed: {count}')
        if len(unknownCountryList) > 0:
            print(f'\nUnknown Country list: (total {len(unknownCountryList)})\n{list(unknownCountryList.keys())}') 
        if len(unknownStatesList) > 0:
            #print(f'\nUnknown states list: (total {len(unknownStatesList)})\n{list(unknownStatesList.keys())}')
            print(f'\nUnknown states found: {len(unknownStatesList)}')
    except FileNotFoundError:
        print('Please check whether the current directory has the "access.log" file')
    except Exception as ex:
        print(f'EXCEPTION: from main function : {ex}')

if __name__ == '__main__':
    if( len(sys.argv) == 2):
        if sys.argv[1].endswith('.log'):    
            try:
                accessLogFile = sys.argv[1]
                if os.path.exists(accessLogFile) and os.path.exists(dbFileName):
                    start = time.time()
                    main(accessLogFile, dbFileName)
                    end =  time.time()
                    print(f'\nTotal execution time: {end-start:.2f} seconds.')
                else:
                    print(f'Please check whether the current directory contains the given access log file and the database file: \'{dbFileName}\'')
            except Exception as ex:
                print(f'EXCEPTION: from __main__ : {ex}')
        else:
            print('Please provide ONLY the \'access.log\' file as the first argument.')
    else:
        print('Please provide ONLY the \'access.log\' file as the first argument.')
