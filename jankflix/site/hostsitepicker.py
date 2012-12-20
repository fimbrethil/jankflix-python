from jankflix.site.hostsite import *
from jankflix.site.template import HostSite, LinkSite

def allSubclasses(cls):
    return cls.__subclasses__() + [g for s in cls.__subclasses__()
                                   for g in allSubclasses(s)]
    
def pickHostSite(host_site_types):
    for host_site_type in host_site_types:
        for host_site in allSubclasses(HostSite):
            if host_site.getName() in host_site_type:
                return host_site_type,host_site

def pickFromLinkSites(link_sites,season,episode):
    for link_site in link_sites:
        assert isinstance(link_site, LinkSite)
        types = []
        types = link_site.getHostSiteTypes(season, episode)
        result = pickHostSite(types)
        if result:
            picked_type,picked_site = result
            index = types.index(picked_type)
            host_at_index = link_site.getHostSiteAtIndex(season, episode, index)
            host_instance = picked_site(host_at_index)
            assert isinstance(host_instance, HostSite)
            return host_instance

