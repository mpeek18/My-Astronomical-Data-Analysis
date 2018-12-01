'''
Created on Nov 8, 2018

@author: Matthew Peek
@change: 24 November 2018
'''
import numpy as np
from matplotlib import pyplot as plt
from queryPackage.SDSSQuery import SDSSQuery

class ObjectMagnitudes:
    
    """
    ObjectMagnitude constructor. Instantiates SDSSQuery class, runs spectra query
    and get results. Argument order latitude, longitude, num.
    
    @param param: latitude in decimal degree format.
    @param param: longitude in decimal degree format. 
    @param param: int expands search area by multiplying with arcminutes.
    """
    def __init__(self, longitude, latitude, radiusMultiplier):
        self.query = SDSSQuery(longitude, latitude, radiusMultiplier)
        self.result = self.query.querySpectra()
        self.objectColor = []
        self.gFilter = []
        self.rFilter = []
        self.objectID = []
        self.objectType = []
    #End ObjectMagnitude constructor
    
    """
    GetGFilter function looks in query result and gets modelMag_g column.
    @return: list of g filter values.
    """
    def getGFilter(self):
        try:
            for i in range(0, len(self.result)):
                self.gFilter.append(self.result[i]['modelMag_g'])
            return self.gFilter
        except:
            return ValueError('No data found for G-Filter')
    #End getGFilter function
    
    """
    GetRFilter function looks in query result and gets modelMag_r column.
    @return: list of r filter values.
    """
    def getRFilter(self):
        try:
            for i in range(0, len(self.result)):
                self.rFilter.append(self.result[i]['modelMag_r'])
            return self.rFilter
        except:
            return ValueError('No data found for R-Filter')
    #End getRFilter function
    
    """
    GetObjectID function looks in query result and gets objID column.
    @return: list of Object ID values. Otherwise returns ValueError.
    """
    def getObjectID(self):
        try:
            for i in range(0, len(self.result)):
                self.objectID.append(self.result[i]['objID'])    
            return self.objectID
        except:
            return ValueError('No Data found for Object IDs')
    #End getObjectID function
    
    """
    GetObjectType function looks in query result and gets Type column.
    @return: list of object types. Otherwise returns ValueError.
    """
    def getObjectType(self):
        try:
            for i in range(0, len(self.result)):
                self.objectType.append(self.result[i]['type'])
            return self.objectType
        except:
            return ValueError('No Data found for Object Type')
    #End getObjectType function
    
    """
    GetObjectColors function subtracts every value in g filter list from every value
    in r filter list to obtain an objects color.
    @return: list of object's color in magnitude.
    """
    def getObjectColors(self):
        self.getGFilter()
        self.getRFilter()
        for i in range(0, len(self.gFilter)):
            objColor = (self.gFilter[i] - self.rFilter[i])
            self.objectColor.append(objColor)
        return self.objectColor
    #End getObjectColors function
    
    """
    PlotMagnitudes function makes a scatter plot using objectColor and 
    gFilter lists. Shows how an objects color changes to more red as 
    it gets farther away. Line of best fit is drawn to illustrate trend.
    """
    def plotMagnitudes(self):
        try:
            self.getObjectColors()
            plt.scatter(self.objectColor, self.gFilter)
            plt.plot(np.unique(self.objectColor), np.poly1d(np.polyfit(self.objectColor, self.gFilter, 2))
                     (np.unique(self.objectColor)), c='r')
            plt.xlabel("Object Color")
            plt.ylabel("Object Magnitude")
            plt.show()
        
        except:
            print("No data found")
    #End plotMagnitudes function
     
    """
    RunObjectMagnitudes function calls plotMagnitudes function.
    X-axis = object colors list.
    Y-axis = g filter list.
    """   
    def runObjectMagnitudes(self):
        self.plotMagnitudes()
        self.getObjectColors()
        self.getGFilter()
        self.getObjectID()
        self.getObjectType()
    #End runObjectMagnitudes function    
            
"""
Test ObjectMagnitudes implementation

target1 = ObjectMagnitudes(143.50993, 55.239775, 10)
target1.plotMagnitudes()
"""
