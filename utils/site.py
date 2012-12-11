'''
Created on Nov 21, 2012

@author: christian
'''
import urllib2
from BeautifulSoup import BeautifulSoup
import urllib

USER_AGENT = "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)"

class Site(object):
    '''
    Generic class for all site 
    '''


    def __init__(self, url = None):
        if url != None:
            page, newUrl = Site.getPageWithRedirectedURL(url)
            self.soup = BeautifulSoup(page)
            self.url = newUrl
            self.values = {'User-Agent' : USER_AGENT}
    @staticmethod
    def getPage(url, postParams = None):
        values = {'User-Agent' : USER_AGENT}
        if postParams == None:
            request = urllib2.Request(url, postParams, values)
        else:
            request = urllib2.Request(url, urllib.urlencode(postParams), values)
        response = urllib2.urlopen(request)
        res = str(response.read())
        response.close()
        res = res.replace("iso-8859-1", "utf-8")
        return res
    @staticmethod
    def getPageWithRedirectedURL(url, postParams = None):
        values = {'User-Agent' : USER_AGENT}
        if postParams == None:
            request = urllib2.Request(url, postParams, values)
        else:
            request = urllib2.Request(url, urllib.urlencode(postParams), values)
        response = urllib2.urlopen(request)
        res = str(response.read())
        redirected = response.geturl()
        response.close()
        res = res.replace("iso-8859-1", "utf-8")
        return (res, redirected)



