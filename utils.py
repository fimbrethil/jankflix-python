'''
Created on Nov 21, 2012

@author: christian
'''


'''
classdocs
'''

def getAfter(string, afterThis):
        return string[string.index(afterThis) + len(afterThis):]

def getBefore(string, beforeThis):
        return string[:string.index(beforeThis)]
