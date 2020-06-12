#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv

def downloadCSVcontent(content, outputFile):
    with open(outputFile, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(content)
        print('Successfully downloaded file: ',outputFile)

def createLIARcsv(outPutfile):        
    content = [['id','content','label']]
    tsv_file = open("valid.tsv")
    r = csv.reader(tsv_file, delimiter="\t")
    tsv_file = open("test.tsv")
    t = csv.reader(tsv_file, delimiter="\t")
    tsv_file = open("train.tsv")
    s = csv.reader(tsv_file, delimiter="\t")
    for row in r:
        if 'false' in row[1]:
            content = content + [[row[0],row[2],1]]
        if 'true' in row[1]:
            content = content + [[row[0],row[2],0]]
    for row in t:
        if 'false' in row[1]:
            content = content + [[row[0],row[2],1]]
        if 'true' in row[1]:
            content = content + [[row[0],row[2],0]]
    for row in s:
        if 'false' in row[1]:
            content = content + [[row[0],row[2],1]]
        if 'true' in row[1]:
            content = content + [[row[0],row[2],0]]
        
    print('Length of csv file:', len(content))
    downloadCSVcontent(content, outPutfile)
    
#createLIARcsv('liar.csv')
    
def getCSVfile(fileName):
    r = csv.reader(open(fileName)) 
    lines = list(r)
    return lines

liar = getCSVfile('liar.csv')

print(len(liar))

