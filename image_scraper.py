import os
import sys
import time
from urllib import FancyURLopener
import urllib2
import simplejson
from selenium import webdriver


def get_image(searchTerm):

    # Replace spaces ' ' in search term for '%20' in order to comply with request
    searchTerm = searchTerm.replace('%','')
    searchTerm = searchTerm.replace(' ','%20')
    
    # Start FancyURLopener with defined version 
    # class MyOpener(FancyURLopener): 
    #     version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'
    # myopener = MyOpener()

    count= 0
    urls = []
    for i in range(0,2):
        # Notice that the start changes for each iteration in order to request a new set of images for each loop
        url = ('https://ajax.googleapis.com/ajax/services/search/images?' + 'v=1.0&q='+searchTerm+'&start='+str(i*4)+'&userip=MyIP')
        print "search url: \n", url
        request = urllib2.Request(url, None, {'Referer': 'testing'})
        response = urllib2.urlopen(request)

        results = simplejson.load(response)
        data = results['responseData']
        dataInfo = data['results']

        for myUrl in dataInfo:
            count += 1
            urls.append(myUrl['unescapedUrl'])

        # Sleep to prevent IP blocking from Google
        time.sleep(1)
        return urls