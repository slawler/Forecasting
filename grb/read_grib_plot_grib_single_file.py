# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 11:09:45 2016

@author: slawler
"""
#---Load Modules
import pygrib
import numpy as np
import pandas as pd
from glob import glob
import matplotlib.pyplot as plt
from datetime import datetime
from dateutil import parser


#---Enter File Number 
f = raw_input('Enter Number of File on list:   ')

#---Read Directory, Create list Grib Files,Open Selected grib file
files = glob('*.grb')
gribfile = files[int(f)]


####-----------------FUNCTION LIST-----------------####
#def PullGribs(dtm):
#    files = glob('*.grb')
#    gribfile = files[int(f)]
    
#Write Function to extract grbs for desired forecast period



########################################################
def ReadGrib(infile):
    grbs = pygrib.open(infile)    
    for grb in grbs:
          print grb
    
    keys = grb.keys() 
    cols = grb.Nx; rows = grb.Ny
    dx   = grb.Dx; dy   = grb.Dy 
    latfirst = grb.latitudeOfFirstGridPointInDegrees
    lonfirst = grb.longitudeOfFirstGridPointInDegrees
    print 'rows ' + str(rows)
    print 'cols ' + str(cols)
    print 'dx   ' + str(dx)
    print 'dy   ' + str(dy)    
    print "Lattitude of First Grid Point ", latfirst
    print "Longitude of First Grid Point", lonfirst    
    grb_vals  = pd.DataFrame(grb.values[:])
    grbs.close()
    return rows, cols, dx, dy, latfirst, lonfirst
########################################################
def GribVals(infile):
    grbs = pygrib.open(infile)    
    for grb in grbs:
          print grb
          
    grb_vals  = pd.DataFrame(grb.values[:])
    return grb_vals
########################################################    
def GribPlot(GribValues):
    fig = plt.figure(figsize=(7,5))
    ax = fig.add_subplot(111)
    ax.set_title('%s' %str(GribValues))
    plt.imshow(grb_vals)
    ax.set_aspect('equal')
    cax = fig.add_axes([0.12, 0.1, 0.78, 0.8])
    cax.get_xaxis().set_visible(False)
    cax.get_yaxis().set_visible(False)
    cax.patch.set_alpha(0)
    cax.set_frame_on(False)
    plt.colorbar(orientation='vertical')
########################################################  
def MakeHourly(infile):
    rows, cols, dx, dy, latfirst, lonfirst = ReadGrib(infile)   
    grb_vals = GribVals(infile)
    cols     = int(cols)
    rows     = int(rows)
    x_cd     = float(855)*dx
    y_cd     = float(550)*dy
    cellsize = float(4762.5) 
    
    grib_hourly = grb_vals*1/6.
    
    #---Write new Subgrid Files
    for i in range(6):
        dtm_parse = infile[4:17]    
        dtm_base  = dateutil.parser.parse(dtm_parse)
        delta     = timedelta(hours = i)
        dtm_out   = dtm_base + delta
        with open('%s' %(dtm_out),'w') as newfile:
            newfile.write('NCOLS '+ str(cols)+ '\n')
            newfile.write('NROWS '+ str(rows)+ '\n')
            newfile.write('XLLCORNER '+ str(x_cd)+ '\n')
            newfile.write('YLLCORNER '+ str(y_cd)+ '\n')
            newfile.write('CELLSIZE '+ str(cellsize)+ '\n')
        
        grib_hourly.to_csv('%s' %(dtm_out), sep = ' ', 
                           header = False, index = False, mode = 'a')
########################################################
def PrintGribKeys(infile):
    grbs = pygrib.open(infile)   
    for grb in grbs:
          print grb
    
    keys = grb.keys()   
    for k in keys:
       try:
          print k + " "+str(grb[k])
       except:
          print "cannot get value for" + k
    grbs.close()    
########################################################

                   
#---------------RUN FUNCTIONS    

files = glob('*.grb')
for f in files:          
    #grb_vals = GribVals(f)
    #GribPlot(grb_vals) 
    #rows, cols, dx, dy, latfirst, lonfirst = ReadGrib(gribfile)
    MakeHourly(f)
    
