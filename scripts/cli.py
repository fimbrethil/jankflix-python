'''
Created on Nov 26, 2012

@author: christian
'''
import argparse
from linksite.onechannel import OneChannel
import atexit
import subprocess
from utils import dl
import os, sys
sys.path.insert(0, os.path.abspath('..'))

'''
Functionality we want to provide:
1. Take a search query and download a specific episode, an entire season, or the entire show. 
    a. Make the search query and ask the user to select the search result they want, 
        or automatically select if there's only one search result
    b. Make the appropriate show/season file structure if downloading more than one episode 
    c. Assemble all linksites behind the scenes and select the best one (perhaps ask the user about this)
    d. Download the episode, putting it in the proper directory. 
        If there are multiple episodes download them at the same time. 
        If there are host sites that only allow one concurrent connection from an IP address, handle this properly. 
2. Translate a supported hostsite link into a file and download that file. 
    a. Parse the url, properly identifying the protocol (if any provided, assuming http if none)
        Additionally, identify the host site and push the url into the appropriate hostsite implementation. 
    b. Translate the url into a download link and print the link. 
3. Translate a supported linksite and search query into results, episode names, an episode summary, or anything else.
    Basically let the user make queries that the program is allowed to about show information. 
    a. Given specific commandline arguments, determine what information the user wants and from where
    b. Make the appropriate queries to the linksite and provide the user with the result. 
'''



def main():
    parser = argparse.ArgumentParser(description = 'Jankflix - A jankier way to watch things!')
    parser.add_argument('query', type = str, help = 'A show you want to watch', nargs = "?")
    parser.add_argument('-s', dest = 'season',type=int, help = 'season to watch')
    parser.add_argument('-e', dest = 'episode',type=int, help = 'episode to watch')
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('-c', dest = 'command',type=str, help = 'command to run when the video starts downloading')
    group.add_argument('-n', dest = 'name',type=str, help = 'name on which to append the season and episode and save to disc')
    args = parser.parse_args()
    query = args.query
    season = args.season
    episode = args.episode
    command = args.command
    name = args.name
    while True:
        if not query:
            query = raw_input("What show do you want to watch: ")
        searchResult = OneChannel.searchSite(query)
        if len(searchResult) == 0:
            print "Search did not return any results."
            query = None
        else:
            break
    for i in range(len(searchResult)):
        title, link = searchResult[i]
        print "%i : %s    (%s)" % (i, title, link)
    selnum = getIntInput("Which one do you want to watch: ", 0, len(searchResult)-1)
    
    title, link = searchResult[selnum]
    print "Accessing show page"
    oc = OneChannel(link)
    seasons = oc.getSeasons()
    print "Seasons: ",seasons
    if season and season not in seasons:
        print "Season does not exist. Please choose another."
        season = None
    if not season:
        season = getIntInput("Which season do you want to watch: ", int(min(seasons)),int(max(seasons)) )
        #this assumes that between the min and max of the season numbers, it is completely filled. 
        
        
    episodes = oc.getEpisodes(season)
    
    names = oc.getEpisodeNames(season)
    for i in range(len(episodes)):
        print episodes[i],":",names[i]
    if episode and episode not in episodes:
        print "Episode does not exist. Please choose another."
        episode = None
    if not episode:
        #TODO: this doesn't work. Need to cast array to int to run min on it. 
        episode = getIntInput("Which episode do you want to watch: ", int(min(episodes)),int(max(episodes)) )
        #this assumes that between the min and max of the season numbers, it is completely filled. 
        
    if not command and not name:
        saveOrRun = getIntInput("Do you want to (0) save or (1) run the episode: ", 0, 1)
        if saveOrRun == 0:
            name = raw_input("Save to what file?")
        else:
            command = raw_input("Run what program (with the file path as an argument)?:")
      
    print "Getting host site"
    hostSite = oc.chooseHostSite(season, episode)
    metadata = hostSite.getMetadata()
    videoURL = hostSite.getVideo()
    if name != None:
        filename = name + "." + metadata["extension"]
    else:
        filename = "video.flv"
    if command:
        processs,status = dl.startDownloads([(videoURL,filename)])
        atexit.register(onexit, proc = processs[0],rmFile = filename)
        subprocess.call([command, filename])
        processs[0].terminate()
    else:
        processs,status = dl.startDownloads([(videoURL,filename)])
        atexit.register(onexit, proc = processs[0])
        while processs[0].is_alive:
            print status[0].get(True,2)

def getIntInput(query, minimum,maximum):
    while True:
        sel = raw_input(query)
        if sel.isdigit():
            selnum = int(sel)
            if selnum >= minimum and selnum <= maximum:
                return selnum
        print "Invalid selection"
        


def onexit(proc,rmFile=None):
    proc.terminate()
    if rmFile:
        os.remove(rmFile)
if __name__ == '__main__':
    main()

