from jankflixmodules.site.linksite.tvlinks import TVLinks
from jankflixmodules.site.linksite.onechannel import OneChannel
import operator
def decide(show):
    #search onechannel for show
    oc_result = OneChannel.searchSite(show)[0]
    print oc_result
    #search tvlinks
    tl_result = TVLinks.searchSite(show)[0]
    print tl_result
    #instanciate both objects passing in the second part of the result tuple, the link
    oc = OneChannel(oc_result[1])
    tl = TVLinks(tl_result[1])
    all_sites = dict()
    #season is the last season of the show
    season =oc.getSeasons()[-1]
    #for all episodes in that season
    for episode in oc.getEpisodes(season):
        for type in oc.getHostSiteTypes(season, episode):
            if "daclips" in type:
                print season, episode, "onechannel"
            if type in all_sites:
                all_sites[type] = all_sites[type] + 1
            else:
                all_sites[type] = 1
            print all_sites
    season =tl.getSeasons()[-1]
    for episode in tl.getEpisodes(season):
        for type in tl.getHostSiteTypes(season, episode):
            if "daclips" in type:
                print season, episode, "tvlinks"
            if type in all_sites:
                all_sites[type] = all_sites[type] + 1
            else:
                all_sites[type] = 1
            print all_sites
    
    sorted_sites =  sorted(all_sites.iteritems(), key=operator.itemgetter(1))
    sorted_sites.reverse()
    print sorted_sites
                    

decide("avatar")
