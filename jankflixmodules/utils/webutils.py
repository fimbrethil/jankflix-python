import urllib2

def exists(site):
    request = urllib2.Request(site)
    request.get_method = lambda : 'HEAD'
    response = urllib2.urlopen(request)
    return response.getcode() == 200
