# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 16:31:02 2016

@author: slawler
"""


#------------Import Py Modules-----------#
import pandas as pd
import sys


#------------Import User Modules---------#
ModPATH   = 'C:\\Users\\sml\\Desktop\\CameronRun\\python'
sys.path.append(ModPATH)
from MPE_FUN import *


#----------------------Processing Steps--------------------------#
#--------------------------1
'''
#--Move all Files to directory based on month and year 
for i in np.arange(2010,2015):
    year = i; year_str = str(year)
    print year_str
    
    PATH = 'C:\\Users\\sml\\Desktop\\MPE\\%s\\%s' % (year_str, year_str)

    files = FindXMRG(PATH)
    PartionFiles(files)
'''
#--------------------------2
'''
#Rename files from MARFC (i.e. 'APR' becomes '4')
for i in np.arange(2010,2016):
    
    year = i; year_str = str(year)
    print year_str
    PATH = 'C:\\Users\\sml\\Desktop\\QPF\\%s' % (year_str)
    
    ChDirMonth2Date(PATH,year_str)
'''
#--------------------------3

'''
Open all Directories and sub directories: Untar & unzip files

from os import path, chdir       
for i in np.arange(2010,2011):
    for j in np.arange(1,13):
        destination = str(j)+str(i)
        year = i; year_str = str(year) 
        PATH = 'C:\\Users\\sml\\Desktop\\QPF\\%s\\%s' % (year_str, destination) 
        if path.exists(PATH): chdir(PATH)        
        try:
            UntarUnzip()
        except:
            print "Empty Directory: ", PATH 
    
'''
#--------------------------4
#--Move all Files to directory based on month and year and forecast period 

#forecast = ['00','06','12','18']
'''
for i in np.arange(2010,2016):
    for j in np.arange(1,13):
        destination = str(j)+str(i)
        year = i; year_str = str(year) 
        PATH = 'C:\\Users\\sml\\Desktop\\QPF\\%s\\%s' % (year_str, destination) 
        
        try:
            files = FindXMRG(PATH)
            SplitForecast(files)
        except:
            print "Empty Directory: ", PATH 
'''
#--------------------------5
# Walk new directories and extract the most recent forecast
#--Use the first 2 from the 00 period, since missing sig data in 06 periods

'''
for i in np.arange(2010,2016):
    for j in np.arange(1,13):
        destination = str(j)+str(i)
        year = i; year_str = str(year) 
        PATH = 'C:\\Users\\sml\\Desktop\\QPF\\%s\\%s' % (year_str, destination)
        newPath = 'C:\\Users\\sml\\Desktop\\QPF\\%s\\%s' % (year_str, year_str)
        for root, dirs, files in os.walk(PATH):
            if  root[-2:] == '00': 
                print '00', root
                for xmrg in files:                    
                    if xmrg[-4:]== 'f006': 
                        shutil.copy(root+'\\'+xmrg,newPath)
                    elif xmrg[-4:]== 'f012':
                        shutil.copy(root+'\\'+xmrg,newPath)
                    else: continue    
                        
            #elif root[-2:] == '06': print '\n', ' These arent the drones youre looking for! ','\n'  
            elif root[-2:] == '12': 
                print '12', root
                for xmrg in files:                    
                    if xmrg[-4:]== 'f006':
                        shutil.copy(root+'\\'+xmrg,newPath)
            elif root[-2:] == '18': 
                print '18', root                                     
                for xmrg in files:                    
                    if xmrg[-4:]== 'f006':
                        shutil.copy(root+'\\'+xmrg,newPath)            
            else: print '\n', ' These arent the drones youre looking for! ','\n' 
        
'''        

#--------------------------5

#--Copy processed files to central folder for transfer to linux

for i in np.arange(2010,2016):
    destination = str(i)
    year = i; year_str = str(year) 
    PATH = 'C:\\Users\\sml\\Desktop\\QPF\\%s\\%s' % (year_str, year_str)
    linux = 'C:\\Users\\sml\\Desktop\\ToLinux\\QPF'
    shutil.move(PATH,linux)
