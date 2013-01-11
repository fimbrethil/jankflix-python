Jankflix
===============

A graphical user interface (GUI) and command line interface (CLI) for easily downloading tv shows favorite video linking and video hosting sites. 

Want to watch episode 2 of season 3 of Avatar the Last Airbender? 
Using either the CLI or the GUI you can do this faster than possible in a browser, and you get to keep the file afterward!

The key is a couple very important abstraction layers that makes the program both relatively reliable amid the shifting sands of changing website layouts. 
* **Link sites** are the term we've given to websites like 1channel.ch and tv-links.eu that provide links to websites which host the files. 
* **Host sites** are the websites which actually host the sites. Currently supported host sites include: putlocker, and gorillavid among others. 
Adding support for another host site is as easy as creating a class in the host site folder, which is integrated automatically into the framework. 

The benifits of this approach include:
* Easy to add support for new sites
* Robust against layout changes of a host site
* Host site code is reused between link site calls

Installation
------------
* Clone the repository and run setup.py. This installs the jankflix package, plus provides two callable commands: **jankflix** and **cjankflix**
* Verify that the default media players for opening flv, mp4, and avi files are what they should be. Media players which handle incomplete video files are preferred as the files will be streaming from a site. 
* From there, just run:

        $ jankflix
        [gui pops up]

  or alternatively:

        $ cjankflix
        What show do you want to watch: avatar
        0 : Watch Avatar: The Last Airbender (2005)
        Automatically choosing Watch Avatar: The Last Airbender (2005)
        Accessing show page
        Seasons:  1, 2, 3
        Which season do you want to watch: 2
        Which episode do you want to watch: 3
        Do you want to (0) save or (1) run the episode: 1
        Run with which program? (vlc): [press enter or alternatively enter another media player]
        (from here, the program should start downloading the file 
        
  another option:
  
        $ cjankflix -s 2 -e 3 -c vlc avatar
Note: This library requires BeautifulSoup, PyQt4



