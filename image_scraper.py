import os
import sys
import time
from urllib import FancyURLopener
import urllib2
import simplejson
from selenium import webdriver


def get_image(searchTerm):
    '''
    INPUT: string, search term
    OUTPUT: list of strings (urls) with top Google search image results

    '''
    # Replace spaces ' ' in search term for '%20' in order to comply with request
    searchTerm = searchTerm.replace('%','').replace(' ','%20')
    
    url = ('https://ajax.googleapis.com/ajax/services/search/images?' + 'v=1.0&q='+searchTerm+'&start='+str(0)+'&userip=MyIP')
    request = urllib2.Request(url, None, {'Referer': 'testing'})
    response = urllib2.urlopen(request)
    results = simplejson.load(response)
    data = results['responseData']
    dataInfo = data['results']
    img_urls = [myUrl['unescapedUrl'] for myUrl in dataInfo]
    return img_urls[0]