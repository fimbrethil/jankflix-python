'''
Created on Nov 26, 2012

@author: christian
'''
import argparse
import urllib2
from multiprocessing import Process
from subprocess import call
from linksite.onechannel import OneChannel
from utils.utils import getAfter, getBefore, download
import atexit
import subprocess
from utils.site import Site
from utils import site
import shutil
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
    parser.add_argument('-c', dest = 'command', help = 'command to run when the video starts downloading', required = False)
    parser.add_argument('-n', dest = 'name', help = 'name on which to append the season and episode and save to disc', required = False)
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
    sel = input("Which one do you want to watch: ")
    title, link = searchResult[sel]
    oc = OneChannel(link)
    #print oc.getHostSite(season, episode)

    videoURL = oc.getHostSite(season, episode)

#    a = '''import urllib2
#import shutil
#    values = {'User-Agent' : "''' + site.USER_AGENT + '''"}
#    request = urllib2.Request("''' + videoURL + '''", None, values)
#    response = urllib2.urlopen(request)
#    filename = response.info()['Content-Disposition']
#    filename = filename[filename.index("filename='") + len("filename='"):]
#    filename = filename[:filename.index("'")]
#    filename = "./" + filename
#    print filename

#with open(filename, 'wb') as f:
#    shutil.copyfileobj(response, f)
#'''
    if name != None:
        filename = name + "s" + season + "e" + episode + ".vlc"
    else:
        filename = "video.flv"
    wgetCommand = ["wget", "-U", '"' + site.USER_AGENT + '"', '-O', filename, videoURL]
    if command:
        proc = subprocess.Popen(wgetCommand)
        atexit.register(onexit, proc = proc)
        subprocess.call([command, filename])
    else:
        subprocess.call(wgetCommand)


def onexit(proc):
    proc.kill()
if __name__ == '__main__':
    main()

