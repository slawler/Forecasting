# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 17:35:23 2016

@author: slawler
"""

# -*- coding: utf-8 -*-
"""

"""

#---Open Ascii file and read HRAP coordinates
def grabdata(infile,x,lines = 4):
    with open(infile) as f:    
        for i in range(lines):
            line = f.readline()
            if i == x:
                data = line.split()
                val = data[1]
                return int(val)
                
    #---Write Coordinate indices for dataframe
def regrid(x_cd,y_cd,cols,rows):
    import numpy as np
    idy = np.arange(x_cd, x_cd + cols)
    idx = np.arange(y_cd-1+rows,y_cd-1,-1)
    return idx, idy
 
   
#---Write New Files for Area of Interest
def SliceGrids(infile, coords): 
    import pandas as pd
    
    xur_hms = coords['xll_hms'] + coords['ncols']-1 
    yur_hms = coords['yll_hms'] + coords['nrows']-1
      
    cols   = grabdata(infile,0)
    rows   = grabdata(infile,1)
    x_cd   = grabdata(infile,2)
    y_cd   = grabdata(infile,3)
    
    row_id, col_id = regrid(x_cd,y_cd,cols,rows)
    
    ##---Read in Precip Grid from ASCII and Slice Sub-Grid
    xmrg = pd.read_csv(infile, skiprows = 5, sep = ' ',
                       names = col_id)
                       
    newgrid = xmrg.set_index(row_id)
         
    newcol = coords['xll_hms']-x_cd
    newrow1 = newgrid.index.get_loc(yur_hms-1) 
    newrow2 = newgrid.index.get_loc(coords['yll_hms'])+1  
   
      
    hms_grid = newgrid.iloc[newrow1:newrow2,newcol:newcol+coords['ncols']]
        
    #---Write new Subgrid Files
    hms_grid.to_csv('%ssubgrid' %(infile), sep = ' ', 
                    header = False, index = False)
    #hms_grid.to_csv('check.txt', sep = '\t')


    
def FixGridAndValues(infile,xll,yll,ncols,nrows):
    import pandas as pd    
    cols     = ncols
    rows     = nrows
    x_cd     = xll*4762.5
    y_cd     = yll*4762.5
    cellsize = float(4762.5) 
    NODATA   = -9999

    ##---Read in Precip Grid from ASCII and Slice Sub-Grid
    xmrg        = pd.read_csv(infile, sep = ' ',header = None)
    #xmrg_hourly = xmrg*1/6.--removed for MPE version
    
    #---Write new Subgrid Files
    with open('%sfmt' %(infile),'w') as newfile:
        newfile.write('NCOLS '+ str(cols)+ '\n')
        newfile.write('NROWS '+ str(rows)+ '\n')
        newfile.write('XLLCORNER '+ str(x_cd)+ '\n')
        newfile.write('YLLCORNER '+ str(y_cd)+ '\n')
        newfile.write('CELLSIZE '+ str(cellsize)+ '\n')
        newfile.write('NODATA_VALUE '+ str(NODATA)+ '\n')
    
    xmrg.to_csv('%sfmt' %(infile), sep = ' ', float_format ='%.6f',
                       header = False, index = False, mode = 'a')
 
# 
def Rename(infile):
    import os, shutil,datetime
    dtm = datetime.datetime.strptime(infile[4:14],'%m%d%Y%H')
    FinalGrid = dtm.strftime('%Y%m%d%H')
    shutil.copyfile(infile,FinalGrid + '.asc') 
                
def WriteBash(files):
    import datetime
    with open('batchload.sh', 'a') as bash:
        for f in files:      
            f_hour  = str(f[0:10])
            dtm_1   = datetime.datetime.strptime(f_hour,'%Y%m%d%H')
            deltat  = datetime.timedelta(hours = 1)
            dtm_2 = dtm_1 + deltat
            dss_start = dtm_1.strftime('%d%b%Y:%H%M')
            dss_stop  = dtm_2.strftime('%d%b%Y:%H%M')
            #---DSS Needs to read the last hour as 2300-2400, not 2300-0000
            if dss_start[10:14]=='2300' and dss_stop[10:14] == '0000':
                dss_stop = dss_stop[:10]+'2400'
            else:
                dss_stop = dss_stop
            
            DSSNAME = dtm_1.strftime('%b%Y')
            command = 'wine asc2dssGrid.exe in='
            dss     = ' dss='
            path    = ' path='
            bash.write(command + str(f) + dss +DSSNAME+'.dss' + path +
            '/HRAP/MARFC/PRECIP/%s/%s/IMPORT/' %(dss_start, dss_stop) + '\n')      
        
        bash.write('#del /S *.asc')
