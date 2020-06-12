#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 24 21:54:43 2020

@author: hrobjartur
"""

text = "sometime around 5 i was walking down the street."
result = text.split()

import csv
from collections import Counter


def splitFake(fileName):
    FAKEwords = []
    REALwords = []
    splitCounter = 0
    kcounter = 0
    r = csv.reader(open(fileName)) 
    lines = list(r)
    print("")
    print('Splitting text to tokens...')
    for row in lines:
        if row[3] == 'FAKE':
            Fwords = (row[2].split())
            
            FAKEwords = FAKEwords + Fwords
        else:
            Rwords = (row[2].split())
            REALwords = REALwords + Rwords
        splitCounter = splitCounter + 1
        if splitCounter == (kcounter + 1000):
            print("Articles split: ", splitCounter)
            kcounter = kcounter + 1000
    print('Articles that have been split: ', splitCounter)
    print("")
    return FAKEwords, REALwords, lines

# fileName = name of .csv file
# mcFake = desired name of output file for most common fake news
# mcReal = desired name of output file for most common real news
# limit = amount of words to be in the most common list
#FUNCTION: Creates two .txt file with a list of 200 most common words
    
def createMostCommonFiles(fileName, mcFake, mcReal, limit):
    splitF, splitR, lines = splitFake(fileName)
    #print((splitF))
    counterF = Counter(splitF)
    counterR = Counter(splitR)

    mostCommonFake = counterF.most_common(limit)
    mostCommonReal = counterR.most_common(limit)
    
    ### CREATES A FILE WITH MOST COMMON FAKE AND REAL .TXT FILE ###
    with open(mcFake, 'w') as f:
        for item in mostCommonFake:
            f.write("%s\n" % item[0])
            
    with open(mcReal, 'w') as f:
        for item in mostCommonReal:
            f.write("%s\n" % item[0])
    print('Successfully create files: ', mcFake, ' and ', mcReal)

def getMostCommonWords(mcFake, mcReal,mcFakeTitle, mcRealTitle):
    fake = open(mcFake, "r")
    real = open(mcReal, "r")
    fakeT = open(mcFakeTitle, "r")
    realT = open(mcRealTitle, "r")
    if fake.mode == 'r':
        mostCommonFake = fake.read()
    if real.mode == 'r':
        mostCommonReal = real.read()
    if fakeT.mode == 'r':
        mostCommonFakeTitle = fakeT.read()
    if realT.mode == 'r':
        mostCommonRealTitle = realT.read()
    print("")
    print('Successfully retrived files: ', mcFake, mcReal, mcFakeTitle, ' and ',mcRealTitle)
    print("")
    return mostCommonFake, mostCommonReal, mostCommonFakeTitle, mostCommonRealTitle

def cleanText(fileName):
    print('cleaning file: ',fileName,'...')
    r = csv.reader(open(fileName)) 
    lines = list(r)
    counter = 0
    kcounter = 0
    for row in lines:
        if row[2] == 'FAKE':
            row[2] = 1
        else:
            row[2] = 0
        splitText = word_tokenize(row[1])
        row[1] = [w for w in splitText if not w in stopWords]
        row[1] = [PorterStemmer().stem(word) for word in row[1]]
        row[1] = " ".join(row[1])
        counter = counter + 1
        if counter == kcounter + 1000:
            kcounter = kcounter + 1000
            print('Cleaned articles so far: ', counter)
    print('finished')
#        
    return lines

def cleanList(lines):
    counter = 0
    kcounter = 0
    print('Cleaning... ',len(lines))
    for row in lines:
        splitText = word_tokenize(row[1])
        row[1] = [w for w in splitText if not w in stopWords]
        row[1] = [PorterStemmer().stem(word) for word in row[1]]
        row[1] = " ".join(row[1])
        counter = counter + 1
        if counter == kcounter + 1000:
            kcounter = kcounter + 1000
            print('Cleaned articles so far: ', counter)
    print('finished')
#        
    return lines

def cleanTitle(fileName):
    print('cleaning file: ',fileName,'...')
    r = csv.reader(open(fileName)) 
    lines = list(r)
    counter = 0
    kcounter = 0
    for row in lines:
        splitText = word_tokenize(row[2])
        row[2] = [w for w in splitText if not w in stopWords]
        row[2] = [PorterStemmer().stem(word) for word in row[2]]
        row[2] = " ".join(row[2])
        counter = counter + 1
        if counter == kcounter + 1000:
            kcounter = kcounter + 1000
            print('Cleaned articles so far: ', counter)
    print('finished')
#        
    return lines

def downloadCSVfile(fileName, outputFile):
    with open(outputFile, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(fileName)
        print('Successfully downloaded file: ',outputFile)
        
def downloadCSVcontent(content, outputFile):
    with open(outputFile, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(content)
        print('Successfully downloaded file: ',outputFile)
        
## Enter fileName and the limit of common words       
fileName = 'baseline2-10000.csv'
limit = 500
##### START WITH CREATING THE MOST COMMON WORDS FILES #####
#FUNCTION: Creates two .txt file with a list of 200 most common  real and fake words
# Call the function: createMostCommonFiles(fileName, mcFake, mcReal, limit)
# fileName = name of .csv file with format: [id,content,label]
# mcFake = desired name of output file for most common fake news words
# mcReal = desired name of output file for most common real news words
# limit = amount of words to be in the most common lists
# EXAMPLE:
#createMostCommonFiles(fileName, 'mostCommonFake-title.txt', 'mostCommonReal-title.txt', limit)
#downloadCSVfile(fileName, 'bcontent2-cleaned.csv')

def getVectorValues(fileName, mostCommonF, mostCommonR, limit):
    print("Calculating values...")
    vecFF_holder = []
    vecRF_holder = []
    vecFR_holder = []
    vecRR_holder = []
    
    FF_values = 0
    RF_values = 0
    FR_values = 0
    RR_values = 0
    
    mostCF = mostCommonF.split()
    mostCR = mostCommonR.split()
    
    valueCounter = 0
    kvalueCounter = 0
    r = csv.reader(open(fileName)) 
    lines = list(r)
    
    for row in lines:
        valueCounter = valueCounter + 1
        if valueCounter == (kvalueCounter + 1000):
            print("Articles examined so far: ", valueCounter)
            kvalueCounter = kvalueCounter + 1000
        if row[2] == "FAKE":
            Fwords = (row[1].split())
            vecFF_tokens = []
            vecFR_tokens = []
            for token in mostCF:
                if token in Fwords:
                    vecFF_tokens = vecFF_tokens + [1]
                    FF_values = FF_values + 1
                else:
                    vecFF_tokens = vecFF_tokens + [0]
            vecFF_holder = vecFF_holder + [vecFF_tokens]
            for token in mostCR:
                if token in Fwords:
                    vecFR_tokens = vecFR_tokens + [1]
                    FR_values = FR_values + 1
                else:
                    vecFR_tokens = vecFR_tokens + [0]
            vecFR_holder = vecFR_holder + [vecFR_tokens]
            
        else:
            Rwords = (row[1].split())
            vecRF_tokens = []
            vecRR_tokens = []
            for token in mostCF:
                if token in Rwords:
                    vecRF_tokens = vecRF_tokens + [1]
                    RF_values = RF_values + 1
                else:
                    vecRF_tokens = vecRF_tokens + [0]
            vecRF_holder = vecRF_holder + [vecRF_tokens]
            for token in mostCR:
                if token in Rwords:
                    vecRR_tokens = vecRR_tokens + [1]
                    RR_values = RR_values + 1
                else:
                    vecRR_tokens = vecRR_tokens + [0]
            vecRR_holder = vecRR_holder + [vecRR_tokens]
                   
            
    fakeLength = len(vecFF_holder)
    realLength = len(vecRF_holder)
    print("")
    print("Amount of fake news:", fakeLength, "Common fake words in Fake news :" ,FF_values)
    print("Amount of real news::", realLength, "Common fake words in Real news:" ,RF_values)
    print("")
    print("Usage% of most common fake news words in fake news: ", (100/(fakeLength * limit)) * FF_values,"%" )
    print("Usage% of most common fake news words in real news: ", (100/(realLength * limit)) * RF_values,"%" )
    print("")
    print("Usage% of most common real news words in fake news: ", (100/(fakeLength * limit)) * FR_values,"%" )
    print("Usage% of most common real news words in real news: ", (100/(realLength * limit)) * RR_values,"%" )
     #fakeLength realLength
        
def predictLabel(fileName, mostCommonF, mostCommonR, mostCommonFTitle, mostCommonRTitle, limit): 
    r = csv.reader(open(fileName)) 
    lines = list(r)
    counter = 0
    kcounter = 0
    fcounter = 0
    rcounter = 0
    predictionCounter = 0
    amountOfRows = len(lines)
    print(amountOfRows)
    mostCF = mostCommonF.split()
    mostCR = mostCommonR.split()
    mostCFT = mostCommonFTitle.split()
    mostCRT = mostCommonRTitle.split()
    for row in lines:
        counter = counter + 1
        R_val = 0
        F_val = 0
        
        split_words = (row[1].split())
        split_title = (row[2].split())
        
        if len(row) > 3497:
            R_val = R_val + 5
            
        for token in mostCF:
            if token in split_words:
                if len(token) > 5:
                    F_val = F_val + 6
                else:
                    F_val = F_val + 1
        for token in mostCR:
            if token in split_words:
                if len(token) > 5:
                    R_val = R_val + 6
                else:
                    R_val = R_val + 1
        for token in mostCFT:
            if token in split_title:
                if len(token) > 5:
                    F_val = F_val + 6
                else:
                    F_val = F_val + 1
        for token in mostCRT:
            if token in split_title:
                if len(token) > 5:
                    R_val = R_val + 6
                else:
                    R_val = R_val + 1
        
        if row[3] == 'FAKE':
            fcounter = fcounter + 1
        if row[3] == 'REAL':
            rcounter = rcounter + 1
        prediction = 'FAKE'
        if R_val > F_val:
            prediction = 'REAL'
        if prediction == row[3]:
            predictionCounter = predictionCounter + 1
        if counter == kcounter + 1000:
            print("calculated so far... ", counter)
            kcounter = kcounter + 1000

        #print('Row: ', counter, ' Type: ' ,row[2], ' Prediction: ', prediction, 'R_val = ', R_val, ' F_val = ', F_val)
    
    print("correct predictions: ", predictionCounter)
    print("Prediction percentage = ", ((predictionCounter / amountOfRows) * 100), "%")
    print('Amount of Real news: ', rcounter, 'Amount of Fake news: ', fcounter, ' SUM: ', rcounter + fcounter)
    
    
mostCommonF, mostCommonR, mostCommonFTitle, mostCommonRTitle = getMostCommonWords("mostCommonFake-50000.txt","mostCommonReal-50000.txt","mostCommonFake-title.txt","mostCommonReal-title.txt")
### Enter fileName and the limit of common words       
#fileName = 'baseline2-100.csv'
limit = 500
###### START WITH CREATING THE MOST COMMON WORDS FILES #####
##FUNCTION: Creates two .txt file with a list of 200 most common  real and fake words
## Call the function: createMostCommonFiles(fileName, mcFake, mcReal, limit)
## fileName = name of .csv file with format: [id,content,label]
## mcFake = desired name of output file for most common fake news words
## mcReal = desired name of output file for most common real news words
## limit = amount of words to be in the most common lists
## EXAMPLE:
#createMostCommonFiles('b2-2-10000-cleaned.csv', 'mCommonFake-title-2.txt', 'mCommonReal-title-2.txt', limit)

##### RETRIVE THE FILES  #####
#FUNCTION: returns two .txt file with a list of 200 most common real and fake words
# getMostCommonWords(mcFake, mcReal)
# mcFake = name of the file with most common fake news words
# mcReal = name of the file with most common real news words
# EXAMPLE:
#mostCommonF, mostCommonR = getMostCommonWords("mostCommonFake-50000.txt","mostCommonReal-50000.txt")

##### GET BAG-OF-WORDS VALUES #####
#FUNCTION: prints usage of common fake words in fake and real news, and real words in fake and real news
# getVectorValues(fileName, mostCommonF, mostCommonR, limit)
# fileName = name of .csv file with format: [id,content,label]
# limit = amount of words to be in the most common lists
# mostCommonF = name of the file with most common fake news words
# mostCommonR = name of the file with most common real news words
# EXAMPLE:
#getVectorValues('baseline2-100.csv', mostCommonF, mostCommonR, limit)

predictLabel('tTest2-10000.csv', mostCommonF, mostCommonR, mostCommonFTitle, mostCommonRTitle ,limit)



