# -*- coding: utf-8 - Python 2.7.11 *-
"""
Description:
Input(s):
Output(s):
slawler@dewberry.com
Created on Mon Jun 20 15:20:13 2016
"""
#------------Load Python Modules--------------------#
import sys, os
from glob import glob
from datetime import datetime as dtm 

MODPATH = 'C:\Users\slawler\Desktop'
sys.path.append(MODPATH)
from Grid2Grid import *
from BuildDSS import *
#------------------------------User Inputs----------------------------------#

fpath = 'P:\\Temp\\slawler\\CASA\\5min' #--NC File Directory
coords = (-96.9635,32.6258,-96.2579,33.1449) #--Grid Coordinates
outpath = 'P:\\Temp\\slawler\\CASA\\5minDSS'#--Output Directory
loadDSS = 'load_files.cmd'

#------------------------------BEGIN SCRIPT----------------------------------#

os.chdir('P:\\Temp\\slawler\\CASA\\5minDSS') 

files = glob(os.path.join(fpath,'*.nc'))

with open (loadDSS,'w') as b:
    for file in files:
        f = file.split('\\')[-1]
        start = dtm.now() 
        Grid(file,coords,500).WriteDSS(f)
        stop = dtm.now()
        name = dssWriter(f[:-3]+'.asc').dss_string()
        b.write(name + '\n')
        print 'Processed time :', stop-start, ' for grid', f
 
os.system(os.path.join(outpath,loadDSS))