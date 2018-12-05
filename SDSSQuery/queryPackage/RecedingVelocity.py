'''
Created on Oct 25, 2018

@author: Matthew Peek
@change: 5 December 2018
'''
import math
import numpy as np
from astropy.io import ascii
from astropy.table import Table
from matplotlib import pyplot as plt
from astropy.cosmology import WMAP9 as cosmo
from queryPackage.SDSSQuery import SDSSQuery

class RecedingVelocity:
    
    """
    Receding Velocity constructor. Instantiates SDSSQuery class, query's object and gets
    query results. Argument order latitude, longitude, num.
    
    @param param: latitude in decimal degree format.
    @param param: longitude in decimal degree format.
    @param param: int expands search area by multiplying with arcminutes  
    """
    def __init__(self, longitude, latitude, radiusMultiplier):
        self.query = SDSSQuery(longitude, latitude, radiusMultiplier)
        self.result = self.query.standardQuery()
        self.ra = []
        self.dec = []
        self.objID = []
        self.redshift = []
        self.velocity = []
        self.objectID = []
        self.c = 300000 #km/s
    #End Constructor
    
    """
    GetID function gets query results and appends object ID's to list.
    
    @return: list of object id's
    """ 
    def getID(self):      
        for i in range(0, len(self.result)):
            self.objID.append(self.result[i]['objid'])                    
        return self.objID
    #End getID function
    
    """
    GetRedshift function gets query results and appends redshifts to list. 
    @return: list of object redshifts.
    """
    def getRedshift(self):
        for i in range(0, len(self.result)):
            self.redshift.append(self.result[i]['z'])
        return self.redshift
    #End getRedshift function
    
    """
    Compute Velocity function goes through object id and redshift lists and calculates
    recessional velocity. Prints object id and velocity.
    """
    def computeVelocity(self):
        #Calculate speed at which galaxies are moving away from us.
        #For redshifts < 1 use equation velocity = (speed of light) * (redshift)
        #Otherwise use velocity = Hubble constant * proper distance
        self.getID()
        self.getRedshift()
        for i in range(0, len(self.redshift)):
            if (self.redshift[i] < 1):
                velocity = self.c * (self.redshift[i])
                self.velocity.append(velocity)
                self.objectID.append(self.objID[i])
            else:
                hubbleConstant = cosmo.H(0)
                hubbleDistance = (self.c / hubbleConstant) * math.log1p(1 + self.redshift[i])
                velocity = hubbleConstant * hubbleDistance
                self.velocity.append(velocity)
                self.objectID.append(self.objID[i])
        return self.velocity, self.objectID
    #End computeVelocity function
    
    """
    GetRA function goes through objectID list matching ra with current objectID.
    @return: list containing ra's for computed object ID's. Otherwise returns ValueError.
    """
    def getRA(self):
        for i in range(0, len(self.objectID)):
            self.ra.append(self.result[i]['ra'])
        return self.ra
    #End getRA function
    
    def getDec(self):
        for i in range(0, len(self.objectID)):
            self.dec.append(self.result[i]['dec'])
        return self.dec
    #End getDec function
    
    """
    Velocity Vs Speed of Light function finds how velocity of object is traveling
    at the speed of light. prints out the object's id and percentage at speed of light.
       
    @param param: Object ID to calculate. If object ID is not contained in the query,
    prints out error message. 
    """
    def velocityVsSpeedOfLight(self, targetID):
        self.computeVelocity()
        vPerSpeedOfLight = 0
        if (targetID in self.objectID):
            for i in range(0, len(self.objectID)):
                if (self.objectID[i] == targetID):
                    objectVelocity = self.velocity[i]
                    vPerSpeedOfLight = (objectVelocity / self.c) * 100
            #print()
            print("Object: " + str(targetID) + " is moving at: " + str(vPerSpeedOfLight)
                   + " % the speed of light", '\n') 
        else:
            print()
            print(targetID, "is not a valid object identifier.")
    #End velocityVsSpeedOfLight function
    
    def viewComputedVelocity(self):
        for i in range(0, len(self.objectID)):
            print ("Object: " + str(self.objectID[i]) + " Velocity: " + str(self.velocity[i]) + " km/s")
    #End viewComputedVelocity function
    
    """
    Plot Velocity function produces a scatter plot of object's redshifts vs. velocities.
    Uses lists of redshifts and velocities, draws quadratic line showing growth.
    """    
    def plotVelocity(self):
        plt.scatter(self.redshift, self.velocity)
        plt.plot(np.unique(self.redshift), np.poly1d(np.polyfit(self.redshift, self.velocity, 3))
                 (np.unique(self.redshift)), c='r')
        plt.xlabel('Object Redshift')
        plt.ylabel('Object Velocity')
        plt.show()
    #End plotVelocity function    
    
    """
    RunRecedingVelocity function calls getID, getRedshift, computeVelocity, and
    plotVelocity functions and runs them.
    """
    def runRecedingVelocity(self):
        self.computeVelocity()
        self.viewComputedVelocity()
        self.plotVelocity()
        self.objectID
        self.getRA()
        self.getDec()
    #End runRecedingVelocity function
    
    def writeData(self):
        self.computeVelocity()
        data = (Table([self.getRA(), self.getDec(), self.objectID], 
                names=['RA', 'Dec', 'Object ID']))
        
        ascii.write(data, 'DataFile.dat', format='fixed_width', overwrite=True)
    #End writeData function
        
    """
    RunSpeedLightPercent function calls velocityVsSpeedOfLight function and runs it.
    
    @param param: object ID to compute. 
    """
    def runSpeedLightPercent(self, targetID):
        self.velocityVsSpeedOfLight(targetID)
    #End runSpeedLightPercent function
            

"""
Test RecedingVelocity Class Implementation

target1 = RecedingVelocity(143.50993, 55.239775, 10)
target1.getID()
target1.getRedshift()
target1.computeVelocity()
target1.velocityVsSpeedOfLight(1237652943176204753)
#target1.plotVelocity()
"""
        