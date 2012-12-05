jankflix-python
===============

A command line interface (CLI) for automatically downloading files from your favorite video linking and video hosting sites. 

Want to watch episode 2 of season 3 of Avatar the Last Airbender? Just enter those three data points into the command line and this program will pull the video file off the site, drop it into VLC, and play it effortlessly!

By introducing a couple key abstraction layers this makes adding support of new sites simple and easy. 

For example, if you wanted to print the result of a search:
```python
from linksite.tvlinks import TVLinks
print TVLinks.searchSite(whatever_search_query)
```

Then, let's say you want to get the seasons for the show you just searched for:
```python
url = "http://www.tv-links.eu" + TVLinks.searchSite(whatever_search_query)[0][1]
tl = TVLinks(url)
print tl.getSeasons()
```

Perhaps you just have a link to a video hosting site that you want translated into an actual file: 
```python
from hostsite.putlocker import PutLocker
pl = PutLocker(putlocker_link)
print pl.getVideo()
```
That's it! You can throw the URL into your favorite media player which supports http streaming and watch it there, or just download it to your computer for later. 

Note: This library requires BeautifulSoup.
