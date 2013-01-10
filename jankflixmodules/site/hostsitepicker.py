from jankflixmodules.site.hostsite import *
from jankflixmodules.site.template import HostSite, LinkSite

def allSubclasses(cls):
    return cls.__subclasses__() + [g for s in cls.__subclasses__()
                                   for g in allSubclasses(s)]
    
def isSupportedHostSite(host_site_type):
    for host_site in allSubclasses(HostSite):
        if host_site.getName() in host_site_type:
            return host_site

def pickFromLinkSite(link_site,season,episode):
    types = link_site.getHostSiteTypes(season, episode)
    assert isinstance(link_site, LinkSite)
    for host_site_type in types:
        print "trying " + host_site_type
        host_site_object = isSupportedHostSite(host_site_type)
        if host_site_object:
            index = types.index(host_site_type)
            host_at_index_link = link_site.getHostSiteAtIndex(season, episode, index)  
            host_site_instance = host_site_object(host_at_index_link)
            print "verifying host site"
            if verifyGoodHostSite(host_site_instance):
                print "hostsite good"  
                return host_site_instance
            else:
                print "host site bad"
    print "No host sites found"
def verifyGoodHostSite(host_site):
    print host_site.__class__
    assert isinstance(host_site, HostSite)
    print host_site.url
    try:
        videoLink = host_site.getVideo()
        print videoLink + " is video link"
        if len(videoLink) == 0:
            return False
        return True
    except Exception as inst:
        print type(inst)     # the exception instance
        print inst.args      # arguments stored in .args
        print inst     
        return False
