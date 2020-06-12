# -*- coding: utf-8 -*-

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

def cleanCategories(text):
    if text is not None:
        cats = re.findall('Categories|Category|Special, ', text)
        for i in cats:
                text = text.replace(i," ")  
        colon = re.findall(':', text)
        for i in colon:
                text = text.replace(i,",")  
    return text


def cleanText(fileName):
    r = csv.reader(open(fileName)) 
    lines = list(r) 
    id = 1
    for e in lines:
        e.insert(0, str(id))
        id = id + 1
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
        if len(e) == 4:
            e.append(None)
        e[4] = cleanCategories(e[4])
    lines[0][4] = 'categories'
    
    return lines


finalText = cleanText('news.csv')
with open('scrapedCleanedNews.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(finalText)
    
print("FINISHED")

