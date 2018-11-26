'''
Created on Nov 26, 2018

@author: Matthew Peek
@change: 26 November 2018
'''

class Error(Exception):
    pass

class ValueNotFound(Error):
    def __init__(self):
        Exception.__init__(self, "Value not found")