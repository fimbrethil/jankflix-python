jankflix-python
===============

A jankier way to watch things!

This project enables the user to fully navigate and download content from link and video hosting sites without ever using a browser!

By introducing a couple key abstraction layers we make adding support of new sites simple and easy. 

For example, if we wanted to print the result of a search:
```python
from linksite.tvlinks import TVLinks
print TVLinks.searchSite(whatever_search_query)
```

Then, let's say we want to get the seasons for the show we just searched for:
```python
url = "http://www.tv-links.eu" + TVLinks.searchSite(whatever_search_query)[0][1]
tl = TVLinks(url)
print tl.getSeasons()
```

Perhaps we just have a link to a video hosting site that we want translated into an actual file: 
```python
from hostsite.putlocker import PutLocker
pl = PutLocker(putlocker_link)
print pl.getVideo()
```
That's it! You can throw the URL into your favorite media player which supports http streaming and watch it there, or just download it to your computer for later. 

Note: This library requires BeautifulSoup.
