# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 21:30:13 2016
Description:
Input:
Output:
@author: sml
"""
#------------Import Python Modules-----------#
from netCDF4 import Dataset
from numpy import floor as flr
from numpy import arange,meshgrid
from scipy import interpolate as intp
from numpy import pi,sin,cos,log
from pandas import DataFrame

#------------Begin Script--------------------#

class Grid(object):

    def __init__(self, grid, coords, cellsize):
        self.grid = grid
        self.coords = coords
        self.cellsize = cellsize

    def lats(self):
        f = Dataset(self.grid,'r')
        lats   = f.variables['Latitude'][:]
        return lats

    def lons(self):
        f = Dataset(self.grid,'r')
        lons   = f.variables['Longitude'][:]
        return lons

    def precip(self):
        f = Dataset(self.grid,'r')
        precip  = f.variables['rain_10min'][:]
        return precip

    def ll_latlon(self):
        lons, lats  = self.lons(),self.lats()
        xmin,ymin = min(lons), min(lats)
        return xmin, ymin

    def ur_latlon(self):
        lons, lats  = self.lons(),self.lats()
        xmax,ymax = max(lons), max(lats)
        return xmax, ymax

    def ToAlbers(self,i,j):
        rad = pi/180
        phi,lda = j*rad,i*rad
        elipsoid,e,e2 = 6378137.0,0.0822719,0.00676866
        phi0, phi1, phi2 =23.0*rad, 29.5*rad,45.5*rad
        lda0= -96.0*rad
        m1=cos(phi1)/(1-e2*sin(phi1)**2)**0.5
        m2=cos(phi2)/(1-e2*sin(phi2)**2)**0.5
        def q_fun(var):
            q=(1-e2)*(sin(var)/(1-e2*sin(var)**2))-\
            ((1/(2*e))*log((1-e*sin(var))/(1+e*sin(var))))
            return q
        q, q0, q1, q2= q_fun(phi),q_fun(phi0),q_fun(phi1),q_fun(phi2)
        n=(m1**2-m2**2)/(q2-q1)
        C=m1**2 +n*q1
        p, p0 =(elipsoid *(C -n*q)**0.5)/n,elipsoid *((C-n*q0)**0.5)/n
        theta = n*(lda- lda0)
        alb_x,alb_y = p*sin(theta),p0-p*cos(theta)
        return alb_x,alb_y

    def toSHG(self,i,j):
        x,y = self.ToAlbers(i,j)
        shg_x, shg_y  = int(flr(x)/self.cellsize),int(flr(y)/self.cellsize)
        return shg_x, shg_y

    def flat_coords(self):
        lons0,lats0 = meshgrid(self.lons(),self.lats())
        lons,lats= (lons0.flatten(),lats0.flatten())
        x,y = self.ToAlbers(lons,lats)
        return x,y

    def flat_precip(self):
        p = self.precip().flatten()
        return p

    '''ALBERS FLATTENED'''
    def ReGrid(self):
        xmin,ymin,xmax,ymax = self.coords
        cellsize =self.cellsize
        lons0,lats0  = self.flat_coords()[0],self.flat_coords()[1]
        llx,lly = self.ToAlbers(xmin,ymin)
        urx,ury = self.ToAlbers(xmax,ymax)
        lons1,lats1 = meshgrid(arange(llx,urx+cellsize,cellsize),arange(lly,ury+cellsize,cellsize))
        SlicePrecip = intp.griddata((lons0,lats0),self.flat_precip(),(lons1, lats1),method='linear')
        return SlicePrecip

    def columns(self):
        xmin,ymin,xmax,ymax = self.coords
        cellsize =self.cellsize
        llx,lly = self.ToAlbers(xmin,ymin)
        urx,ury = self.ToAlbers(xmax,ymax)
        alb_x = arange(llx,urx+cellsize, cellsize)
        cols = []
        for i,x in enumerate(alb_x):
            x,y = self.toSHG(alb_x[i],ury)
            cols.append(x)
        return cols

    def rows(self):
        xmin,ymin,xmax,ymax = self.coords
        cellsize =self.cellsize
        llx,lly = self.ToAlbers(xmin,ymin)
        urx,ury = self.ToAlbers(xmax,ymax)
        alb_y = arange(lly,ury+cellsize, cellsize)
        rows = []
        for i,x in enumerate(alb_y):
            x,y = self.toSHG(urx, alb_y[i])
            rows.append(y)
        return rows

    def DSSgrid(self):
        cols = self.columns()
        rows = self.rows()
        df = DataFrame(self.ReGrid(),index=rows,columns=cols)
        return df

    def WriteDSS(self,name):
        grid       = self.DSSgrid()
        ncols       = len(self.columns())
        nrows       = len(self.rows())
        cellsize   = self.cellsize
        x_cd, y_cd = self.toSHG(self.coords[0],self.coords[1])
        NODATA     = -9999
        ascFile    = '%s.asc' %(name.split('.')[0])
        with open(ascFile,'w') as newfile:
            newfile.write('NCOLS '+ str(ncols)+ '\n')
            newfile.write('NROWS '+ str(nrows)+ '\n')
            newfile.write('XLLCORNER '+ str(x_cd*cellsize)+ '\n')
            newfile.write('YLLCORNER '+ str(y_cd*cellsize)+ '\n')
            newfile.write('CELLSIZE '+ str(cellsize)+ '\n')
            newfile.write('NODATA_VALUE '+ str(NODATA)+ '\n')
        
        grid.to_csv(ascFile, sep = ' ', float_format ='%.6f',
                       header = False, index = False, mode = 'a')
        return ascFile


