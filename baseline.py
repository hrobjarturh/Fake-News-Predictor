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
        if row[2] == 1:
            Fwords = (row[1].split())
            
            FAKEwords = FAKEwords + Fwords
        else:
            Rwords = (row[1].split())
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

#createMostCommonFiles('liar.csv','liarMCF.txt','liarMCR.txt',200)

def getMostCommonWords(mcFake, mcReal):
    fake = open(mcFake, "r")
    real = open(mcReal, "r")
    if fake.mode == 'r':
        mostCommonFake = fake.read()
    if real.mode == 'r':
        mostCommonReal = real.read()
    print("")
    print('Successfully retrived files: ', mcFake, ' and ', mcReal)
    print("")
    return mostCommonFake, mostCommonReal


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
        
def predictLabel(fileName, mostCommonF, mostCommonR, limit): 
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
    print(len(lines))
    for row in lines:
        counter = counter + 1
        R_val = 0
        F_val = 0
        
        split_words = (row[1].split())
        
        if len(row[1]) > 3497:
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
        
        if row[2] == 1:
            fcounter = fcounter + 1
        if row[2] == 0:
            rcounter = rcounter + 1
        prediction = 1
        if R_val > F_val:
            prediction = 0
        if prediction == row[2]:
            predictionCounter = predictionCounter + 1
        if counter == kcounter + 1000:
            print("calculated so far... ", counter)
            kcounter = kcounter + 1000
        #print('Row: ', counter, ' Type: ' ,row[2], ' Prediction: ', prediction, 'R_val = ', R_val, ' F_val = ', F_val)
    
    print("correct predictions: ", predictionCounter)
    print("Prediction percentage = ", ((predictionCounter / amountOfRows) * 100), "%")
    print('Amount of Real news: ', rcounter, 'Amount of Fake news: ', fcounter, ' SUM: ', rcounter + fcounter)
    


def downloadCSVcontent(content, outputFile):
    with open(outputFile, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(content)
        print('Successfully downloaded file: ',outputFile)
        
def predictKeggle(fileName, mostCommonF, mostCommonR, limit): 
    r = csv.reader(open(fileName)) 
    lines = list(r)
    counter = 0
    kcounter = 0
    fcounter = 0
    rcounter = 0
    predictionCounter = 0
    
    cleanedContent = []
    cleanedArticles = getCSVfile('cleaned-keggle.csv')
    print(len(cleanedArticles))
    
    for row in cleanedArticles:
        cleanedContent = cleanedContent + [row[1]]
    
    amountOfRows = len(lines)
    print(amountOfRows)
    mostCF = mostCommonF.split()
    mostCR = mostCommonR.split()
    finalFile = [['id','label']]
    fake = 0
    real = 0
    
    for row in range(amountOfRows):
        counter = counter + 1
        R_val = 0
        F_val = 0
        
        split_words = (lines[row][1].split())
        
        if len(lines[row][1]) > 3497:
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
        if F_val > R_val:
            finalFile = finalFile + [[lines[row][0],'REAL']]
            real = real + 1
        else:
            fake = fake + 1
            finalFile = finalFile + [[lines[row][0],'FAKE']]            
        
    print('total FAKE: ',fake,'total REAL: ',real)
        
    downloadCSVcontent(finalFile, 'baseLineTest2.csv')
    
## Enter fileName and the limit of common words       
fileName = 'baseline2-100.csv'
limit = 500

##### START WITH CREATING THE MOST COMMON WORDS FILES #####
#FUNCTION: Creates two .txt file with a list of 200 most common  real and fake words
# Call the function: createMostCommonFiles(fileName, mcFake, mcReal, limit)
# fileName = name of .csv file with format: [id,content,label]
# mcFake = desired name of output file for most common fake news words
# mcReal = desired name of output file for most common real news words
# limit = amount of words to be in the most common lists
# EXAMPLE:
#createMostCommonFiles(fileName, 'mostCommonFake-t.txt', 'mostCommonReal-t.txt', limit)

##### RETRIVE THE FILES  #####
#FUNCTION: returns two .txt file with a list of 200 most common real and fake words
# getMostCommonWords(mcFake, mcReal)
# mcFake = name of the file with most common fake news words
# mcReal = name of the file with most common real news words
# EXAMPLE:
mostCommonF, mostCommonR = getMostCommonWords("Fbaseline2-50000-noStopwords.txt","Rbaseline2-50000-noStopwords.txt")

##### GET BAG-OF-WORDS VALUES #####
#FUNCTION: prints usage of common fake words in fake and real news, and real words in fake and real news
# getVectorValues(fileName, mostCommonF, mostCommonR, limit)
# fileName = name of .csv file with format: [id,content,label]
# limit = amount of words to be in the most common lists
# mostCommonF = name of the file with most common fake news words
# mostCommonR = name of the file with most common real news words
# EXAMPLE:
#getVectorValues('baseline2-100.csv', mostCommonF, mostCommonR, limit)

predictLabel('liar.csv', mostCommonF, mostCommonR, limit)



