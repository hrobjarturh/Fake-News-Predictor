#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 17:23:12 2020

@author: hrobjartur
"""

import scrapy
from urllib.parse import urljoin


class QuotesSpider(scrapy.Spider):
    name = "category"
    

    start_urls = [
        'https://en.wikinews.org/wiki/Category:Politics_and_conflicts',
    ]

    def parse(self, response):
        letters = ['H','I','J','K','L','M','N','O','P']
        for auth in response.css('div.mw-category-group'):
            if auth.css('h3::text').get() in letters:
                allHrefsInCategory = auth.css('a::attr(href)').getall()
                for href in allHrefsInCategory:
                    nextPageUrl = response.urljoin(href)
                    yield scrapy.Request(url = nextPageUrl, callback = self.parse_middle)
                    
    def parse_middle(self, response):
        subcat = response.css('div[id="mw-subcategories"] a::attr(href)').getall()
        if len(subcat) > 0:
            for hrefs in subcat:
                nextPageUrl = response.urljoin(hrefs)
                yield scrapy.Request(url = nextPageUrl, callback = self.parse_middle) 
            
        for pages in response.css('div[id="mw-pages"]'):
            allHrefsInCategory = pages.css('a::attr(href)').getall()
            for href in allHrefsInCategory:
                nextPageUrl = response.urljoin(href)
                yield scrapy.Request(url = nextPageUrl, callback = self.parse_articles) 
            
                
    def parse_articles(self, response):
        yield{
                'title': response.css('h1::text').get(),
                'date': response.css('span[id="publishDate"]').xpath("@title").get(),
                'content': response.css('p::text,a[class="mw-redirect"]::text').extract(),
                'Categories': response.css('div[class="mw-normal-catlinks"] a::attr(title)').extract()
                
        }
        
#scrapy crawl articles -o articles.csv
#from terminal to download as .csv file
            