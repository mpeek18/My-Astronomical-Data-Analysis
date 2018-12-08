'''
Created on Nov 30, 2018

@author: Matthew Peek
@change: 30 November 2018
'''
import numpy as np
import pickle as pick
from astroquery.sdss import SDSS
from astropy.io import fits
from queryPackage.SDSSQuery import SDSSQuery
from matplotlib import pyplot as plt
from queryPackage.ObjectMagnitudes import ObjectMagnitudes

class ObjectImage:
    
    def __init__(self, longitude, latitude, radiusMultiplier):
        self.query = SDSSQuery(longitude, latitude, radiusMultiplier)
        self.result = self.query.standardQuery()
        
    def getImage(self):
        image = SDSS.get_images(matches=self.result)
        print(image)
        
target1 = ObjectImage(143.50993, 55.239775, 6)
target1.getImage()

