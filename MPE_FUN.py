# -*- coding: utf-8 -*-
"""
Created on Sat Mar 05 07:26:31 2016

1. FindXMRG: Makes a list of extensionless files, formatted as MPE from MARFC
      OUTPUT: list of XMRG files in cwd
  
2. PartitionFiles: 
    See description below

3. ChDirMonth2Date: Rename Directories containing QPF's' 
    See description below
    
@author: sml
"""


def FindXMRG(PATH):
    from os import chdir, path
    from glob import glob
    
    chdir(PATH)
    files = glob('*')    
    dropfiles = []
    for f in files:
        ext =path.splitext(f)[-1]
        if path.isdir(f)==True:
            dropfiles.append(f)
        elif ext !='':
            dropfiles.append(f)
            
    for f in dropfiles: files.remove(f)
    return files        

'''
This function creates directory for a given time period (month here, can change this later),
moves MPE files from that time period to the new directory --then-- deletes the original file.  

Addons: Zip up remaining files when process completes 
'''

#==========================================================================================#
def PartionFiles(files):
    from os import path,mkdir,remove
    from shutil import copy
    from datetime import datetime
    
    print "Begin Process \n"
    i = 0    
    for f in files:
        i+=1 
        date = f[4:14]
        dtm  = datetime.strptime(date,'%m%d%Y%H')
        month=str(dtm.month);year=str(dtm.year)
        movehere = month+year
        if i % 100 == 0:
            print 'Files Moved: ', i
            print  'Writing to Directory: ', movehere
        if path.exists(movehere):
            copy(f,movehere); remove(f)
        else:
            print 'Creating Directory', movehere
            mkdir(movehere)
            copy(f,movehere); remove(f)
    print "Process Complete \n"        

#==========================================================================================#

'''
This function changes the file naming convention for monthly data from character to interger
and adds the year: example if Apr is in the directory 2014, the floder Apr will be renamed 42014.  
'''

def ChDirMonth2Date(PATH,year_str):
    from glob import glob
    from os import chdir, rename
    chdir(PATH)
    files = glob('*') 
    months = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,
    'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}       
    
    for m in months:    
        for f in files:
            if m in f:
                print m
                month = str(months[f])
                newname = month+year_str
                rename(m,newname)                
                print newname

#==========================================================================================#   


'''
This function untars & unzips files within a directory that have the extension .tar.gz
then archives the original files 
'''


def UntarUnzip():
    from glob import glob
    from os import remove
    import tarfile
    files = glob('*tar.gz')
    make_archive = tarfile.open('archive.tar.gz','w:gz')
    for f in files:
        print f
        tar = tarfile.open(f)        
        tar.extractall()
        tar.close()
        make_archive.add(f)
    make_archive.close() 
    
    for f in files:
        remove(f)
        
#==========================================================================================#                
def SplitForecast(files):
    from os import path,mkdir,remove
    from shutil import copy
    from datetime import datetime
    
    print "Begin Process \n"
    i = 0    
    for f in files:
        if f[4] !='6': #===Set Forecast period here
            i+=1 
            date = f[7:15]; f_period = f[14:16]
            #dtm  = datetime.strptime(date,'%Y%d%m%H')
            #month=str(dtm.month);year=str(dtm.year)
            movehere = '24_48_f_periods'
            
            if i % 100 == 0:
                print 'Files Moved: ', i
                print  'Writing to Directory: ', movehere
                    
            if path.exists(movehere):
                copy(f,movehere); remove(f)
            else:
                print 'Creating Directory', movehere
                mkdir(movehere)
                copy(f,movehere); remove(f)
    print "Process Complete \n"            