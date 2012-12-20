'''
Created on Dec 3, 2012

@author: christian
'''
from setuptools import setup, find_packages
for m in ('BeautifulSoup', 'urllib', 'urllib2', 'urlparse'):
    try:
        __import__(m)
    except ImportError:
        pass
install_requires = [
    'BeautifulSoup',
]

setup(name = 'jankflix',
      version = '1.0',
      packages = find_packages(exclude = ("tests",)),
      install_requires = install_requires,
      entry_points = {
        'console_scripts': [
            'jankflix = jankflix.cli.cli:main'
        ]}
      )
