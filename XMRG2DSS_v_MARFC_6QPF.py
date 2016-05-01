# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 17:35:30 2016

@author: slawler
"""


import numpy as np
from glob import glob
import os
import tarfile


PATH   = '/home/slawler/Documents/scripts/pyscripts/'
import sys
sys.path.append(PATH)
 
from XMRG_FUNC_v_MARFC_6QPF import *

#x=852,y=455

#---Assign Bounding limits for HMS Model
xll_hms,ncols   = 955,10
yll_hms, nrows  = 540,10 

coords = {'xll_hms':xll_hms,'ncols':ncols,'yll_hms':yll_hms,'nrows':nrows}
#----------------------------------------------------------------#
#--------------------RUN SCRIPT----------------------------------#
#----------------------------------------------------------------#


#---Tar,Zip&Copy XMRG Files, remove originals   
tarfiles = glob('*.xmrg')
zipup = tarfile.open('xmrg_files.tar.gz','w:gz')
for t in tarfiles:
    zipup.add(t)
    os.remove(t)
zipup.close()    


#---Read converted XMRG files, write .ascsubgrid file & rm asc files
file_list = glob('*.asc')
for f in file_list:  
    SliceGrids(f,coords)
    os.remove(f)
    

#---Write Formated file w/header to .ascsubgridfmt file & rm ascsubgrid files
file_list = glob('*.ascsubgrid')
for f in file_list: 
    FixGridAndValues(f,xll_hms,yll_hms,ncols,nrows)      
    os.remove(f)
    

#---Recompute gridcells & Write Hourly Files
file_list = glob('*.ascsubgridfmt')      
for f in file_list:
    MakeHourly(f)    
      

#---Remove tmp files
file_list = glob('*.tmp')
for f in file_list:
    os.remove(f)
    

files = glob('*.asc')
WriteBash(files)
