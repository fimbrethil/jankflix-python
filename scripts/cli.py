'''
Created on Nov 26, 2012

@author: christian
'''
import argparse
from linksite.onechannel import OneChannel
import atexit
import subprocess
from utils import dl
import os


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
    parser.add_argument('query', metavar = 'search_string', type = str,
                       help = 'a string to search for in linksites')
    parser.add_argument('-s', dest = 'season', help = 'season to watch', required = True)
    parser.add_argument('-e', dest = 'episode', help = 'episode to watch', required = True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-c', dest = 'command', help = 'command to run when the video starts downloading', required = False)
    group.add_argument('-n', dest = 'name', help = 'name on which to append the season and episode and save to disc', required = False)
    args = parser.parse_args()
    query = args.query
    season = args.season
    episode = args.episode
    command = args.command
    name = args.name
    searchResult = OneChannel.searchSite(query)
    for i  in range(len(searchResult)):
        title, link = searchResult[i]
        print "%i : %s    (%s)" % (i, title, link)
    while True:
        sel = raw_input("Which one do you want to watch: ")
        if sel.isdigit():
            selnum = int(sel)
            if selnum >= 0 and selnum < len(searchResult):
                break
        print "Invalid selection"
    
    title, link = searchResult[selnum]
    print "Accessing show page"
    oc = OneChannel(link)
    print "Getting host site"
    videoURL = oc.getHostSite(season, episode)
    
    if name != None:
        filename = name + "s" + season + "e" + episode + ".flv"
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


def onexit(proc,rmFile=None):
    proc.terminate()
    if rmFile:
        os.remove(rmFile)
if __name__ == '__main__':
    main()

