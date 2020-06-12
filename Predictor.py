#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 28 13:21:59 2020

@author: hrobjartur
"""

import csv
import string
import re
import nltk
import math 
import ast
import numpy as np
import pandas as pd
import sys
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
from nltk.stem import PorterStemmer 
import numpy as np
from sklearn.naive_bayes import GaussianNB
from time import time
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, accuracy_score, recall_score, precision_score
import json
from sklearn.linear_model import SGDClassifier
from sklearn import metrics

stopWords = (stopwords.words('english'))

def cleanText(fileName):
    print('cleaning file: ',fileName,'...')
    r = csv.reader(open(fileName)) 
    lines = list(r)
    counter = 0
    kcounter = 0
    for row in lines:
        if row[2] == '1':
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

#finalText = cleanText('baseline2-50000.csv')

def downloadCSVfile(fileName, outputFile):
    with open(outputFile, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(cleanText(fileName))
        print('Successfully downloaded file: ',outputFile)
        
def downloadCSVcontent(content, outputFile):
    with open(outputFile, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(content)
        print('Successfully downloaded file: ',outputFile)
        
#downloadCSVfile('baseline2-10000.csv', 'cleaned-10000.csv')

def getCSVfile(fileName):
    r = csv.reader(open(fileName)) 
    lines = list(r)
    return lines
    

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

#mostCommonF, mostCommonR = getMostCommonWords('Fbaseline2-50000-noStopwords.txt','Rbaseline2-50000-noStopwords.txt')

def downloadDocumentFrequency(FAKE_DFoutputFile, REAL_DFoutputFile, cleanedCorpusFile):
    
    DF_vecF = []
    DF_vecR = []
    r = csv.reader(open(cleanedCorpusFile)) 
    lines = list(r)
    amountOfArticles = len(lines)
    print('amount of articles: ',amountOfArticles)
    Fwords = (mostCommonF.split())
    Rwords = (mostCommonR.split())
    
    for word in Fwords:
        freq = 0
        for article in lines:
            if word in article[1]:
                freq = freq + 1
        DF_vecF = DF_vecF + [math.log(amountOfArticles/(freq + 1))]
    for word in Rwords:
        freq = 0
        for article in lines:
            if word in article[1]:
                freq = freq + 1
        DF_vecR = DF_vecR + [math.log(amountOfArticles/(freq + 1))]
    
    with open(FAKE_DFoutputFile, 'w') as f:
        f.write(str(DF_vecF))
                  
    with open(REAL_DFoutputFile, 'w') as f:
        f.write(str(DF_vecR))
        
    print('Successfully create files: ', FAKE_DFoutputFile, ' and ', REAL_DFoutputFile)

def getDocumentFrequency(DF_Fake, DF_Real):
    fake = open(DF_Fake, "r")
    real = open(DF_Real, "r")
    if fake.mode == 'r':
        Fake_DF = fake.read()
    if real.mode == 'r':
        Real_DF = real.read()
        
    print("")
    print('Successfully retrived files: ', DF_Fake, ' and ', DF_Real)
    print("")
    
    return Fake_DF, Real_DF

#downloadDocumentFrequency('FAKE_DF_50000.txt','REAL_DF_50000.txt','baseline2-50000-noStopwords.csv')
#Fake_DFstr, Real_DFstr = getDocumentFrequency('FAKE_DF_50000.txt', 'REAL_DF_50000.txt')


def termFrequency(cleanedArticle):
    #print("Calculating Term Frequency...")
    TF_vecF = []
    TF_vecR = []
    
    F_values = 0
    R_values = 0

    mostCF = mostCommonF.split()
    mostCR = mostCommonR.split()
    
    words = cleanedArticle.split()
    lengthOfArticle = len(words)
    
    for c_token in mostCF:
        if c_token in words:
            TF_vecF = TF_vecF + [((words.count(c_token)))]
            F_values = F_values + 1
        else:
            TF_vecF = TF_vecF + [0]
    for c_token in mostCR:
        if c_token in words:
            TF_vecR = TF_vecR + [((words.count(c_token)))]
            R_values = R_values + 1
        else:
            TF_vecR = TF_vecR + [0]      
    
    #print('length of vectors:', len(TF_vecF),'and', len(TF_vecR))
    return TF_vecF, TF_vecR
    

#Fake_DF = ast.literal_eval(Fake_DFstr)
#Real_DF = ast.literal_eval(Real_DFstr)

    
def predict():
    #articles = getCSVfile('cleaned-50000.csv')
    
    tfidf = TfidfVectorizer(ngram_range=(1,2), max_df= 0.7, min_df= 0.01)
    
    colnames = ['id','content','label']
    data = pd.read_csv('cleaned-50000.csv', names=colnames)
    
    cleanedArticles = getCSVfile('liar-cleaned.csv')
    
    labels = data.label.tolist()
    contents = data.content.tolist()
    
    #tfidf_content = tfidf.fit_transform(cleanedArticles[:8000])
    #tfidf_content2 = tfidf.fit_transform(contents)
    
    cleanedContent = []
    cleanedLabels = []
    print(len(cleanedArticles))
    
    for row in cleanedArticles:
        cleanedContent = cleanedContent + [row[1]]
        cleanedLabels = cleanedLabels + [row[2]] 
        
    tfidf_content = tfidf.fit_transform(cleanedContent[:8000])
        
    tfidf_cleanedArticles = tfidf.transform(cleanedContent[8000:])
    
    contents_train = tfidf_content
    contents_test = tfidf_content
    labels_train = cleanedLabels[:8000]
    labels_test = labels[:7000]
    
    model = SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, random_state=42,max_iter=5, tol=None)
    model.fit(contents_train, labels_train)
    score_train = model.score(contents_train, labels_train)
    print('score of training', score_train * 100,'%')
    content_predictions = model.predict(tfidf_cleanedArticles)
    
    #print('score of predictions: ', content_train_predictions)
    
    amountTested = len(content_predictions)
#    percentageCorr = np.mean(content_predictions == labels_test)
#    #incorrectPredictions = (len((np.where(labels_test != content_predictions))[0]))
##    print('precentage correct = ', ((amountTested-incorrectPredictions)/amountTested)*100)
#    print('precentage correct = ', (percentageCorr))
    #print('results: ',content_predictions)
    
#    data2 = pd.read_json("test_set.json")
#    data2list = data2.values.tolist()
#    
#    ids = data2.id.tolist()
#    articles = data2.article.tolist()
    
    #print(content_predictions[:1000])
#    finalFile = [['id','label']]
    fake = 0
    real = 0
    fake2 = 0
    real2 = 0
    correct = 0
    for row in range(amountTested):
        if content_predictions[row] == 1:
            fake = fake + 1
 #           finalFile = finalFile + [[cleanedArticles[row][0],'FAKE']]
        else:
            real = real + 1
#            finalFile = finalFile + [[cleanedArticles[row][0],'REAL']]
        if cleanedLabels[row] == '1':
            fake2 = fake2 + 1
        else:
            real2 = real2 + 1
        if str(content_predictions[row]) == cleanedLabels[row]:
            correct = correct + 1
    print('Correct = ', (correct/amountTested)*100)
    
    print('total FAKE: ',fake,'total REAL: ',real,'\n actual total FAKE: ',fake2,'actal total REAL: ',real2)
    #print('finalFile: ',finalFile)
            
    #downloadCSVcontent(finalFile, 'hroiPredictor8.csv')


predict()





