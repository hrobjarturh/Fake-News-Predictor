#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 11:51:19 2020

@author: hrobjartur
"""


import csv
import string
import re

def cleanNumbers(text):
    text = " "+text+" "
    for number in string.digits:
        if number in text:
            count = text.count(number)
            for x in range(count):
                if number in text:
                    placement = text.find(number)
                    if placement != -1:
                        nextIsDigit = True
                        substring = " <NUM>"
                        while nextIsDigit:
                            if text[placement + 1] in string.digits:
                                text = text[:placement] + text[1 + placement:]
                            else:
                                text = text[:placement - 1] + substring + text[1 + placement:]
                                nextIsDigit = False
    return(text)

def cleanEmails(text):
    emails = re.findall(r'[\w\.-]+@[\w\.-]+', text)
    for i in emails:
        text = text.replace(i,"<EMAIL>")  
    return text
        
def cleanUrls(text):
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
    for i in urls:
        text = text.replace(i,"<URL>")  
    return text

def cleanDates(text):
    dates = re.findall(r'\d{4}-\d{2}-\d{2}', text)
    for i in dates:
        text = text.replace(i,"<DATE>")  
    dates2 = re.findall(r'\d{4}.\d{2}.\d{2}', text)
    for i in dates2:
        text = text.replace(i,"<DATE>")  
    dates3 = re.findall(r'\d{4}_\d{2}_\d{2}', text)
    for i in dates3:
        text = text.replace(i,"<DATE>")  
    return text

def cleanText(fileName):
    r = csv.reader(open(fileName)) 
    lines = list(r)  
    for e in lines:
        e.pop(0)
        e.pop(0)
        if len(e) != 15:
            lines.pop(lines.index(e))
    for e in lines:
        print(len(e))
        for x in range(len(e)):
            if "," in e[x]:
                e[x] = e[x].replace(",","")
            if "\n" in e[x]:
                e[x] = e[x].replace("\n","")
        e[3] = e[3].lower()
        e[3] = cleanDates(e[3])
        e[3] = cleanEmails(e[3])
        e[3] = cleanUrls(e[3])
        e[3] = cleanNumbers(e[3])
    return lines

    
finalText = cleanText('1mio-raw-first100.csv')

#entity set article
def fillArticle():
    articleEntitySet = []
    for a in finalText:
        subset = [] 
        subset.append(a[2])
        subset.append(a[3])
        subset.append(a[9])
        subset.append(a[12])
        subset.append(a[13])
        articleEntitySet.append(subset)
    articleEntitySet.pop(0)
    return articleEntitySet
    
articleEntity = fillArticle()

with open('newsCorpus-100.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(finalText)
    
print("FINISHED")
