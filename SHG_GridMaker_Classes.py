
from netCDF4 import Dataset
from pyproj import Proj
from numpy import floor as flr
from numpy import array


class Grid(object):
   
    def __init__(self, grid, cellsize):
        self.grid = grid
        self.cellsize = cellsize
    def dec_lats(self):   
        f = Dataset(self.grid,'r')
        lats   = f.variables['Latitude'][:]
        return lats
    
    def dec_lons(self):   
        f = Dataset(self.grid,'r')
        lons   = f.variables['Longitude'][:]
        return lons
        
    def LowerLeft_LatLon(self): 
        lons, lats  = self.dec_lons(),self.dec_lats()
        xmin,ymin = min(lons), min(lats)
        return xmin, ymin
              
    def proj_shift(self,i,j):
        proj = Proj('+proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=23.0 + \
                 lon_0=-96 +x_0=0 + y_0=0+ellps=GRS80 +datum=NAD83 + \
                 units=m +no_defs ')
        proj_x, proj_y  = proj(i,j)         
        return proj_x, proj_y        
     
    def DecDeg2SHG(self,i,j):
        x, y  = self.proj_shift(i,j)
        grid_x, grid_y  = int(flr(x)/self.cellsize),int(flr(y)/self.cellsize)  
        return grid_x, grid_y  

    def LowerLeft_SHG(self): 
        ll_x,ll_y = self.LowerLeft_LatLon()
        shg_ll_x, shg_ll_y = self.DecDeg2SHG(ll_x,ll_y)
        return shg_ll_x, shg_ll_y   
        
    def columns(self): 
        cols= []
        lons, lats  = self.dec_lons(), self.dec_lats()
        for x in lons:
            col, row = self.DecDeg2SHG(x,lats[0])
            cols.append(col)
        return array(cols)
    
    def rows(self): 
        rows = []
        lons, lats  = self.dec_lons(), self.dec_lats()
        for y in lats:
            col, row = self.DecDeg2SHG(min(lons),y)
            rows.append(row)
            print(col,row)
        return array(rows)
        
   


nc = '29May2015_071200_10min.nc'
g = Grid(nc,500)
'''     def ToAlbers(i,j):
        from numpy import pi,sin,cos,log
        rad = pi/180
        phi,lda = j*rad,i*rad        
        elipsoid,e,e2 = 6378137.0,0.0822719,0.00676866
        phi0, phi1, phi2 =23.0*rad, 29.5*rad,45.5*rad
        lda0= -96.0*rad
        m1=cos(phi1)/(1-e2*sin(phi1)**2)**0.5
        m2=cos(phi2)/(1-e2*sin(phi2)**2)**0.5           
        def q_fun(var):
            q=(1-e2)*(sin(var)/(1-e2*sin(var)**2))-((1/(2*e))*log((1-e*sin(var))/(1+e*sin(var))))
            return q
            
        q,q0 ,q1,q2= q_fun(phi),q_fun(phi0),q_fun(phi1),q_fun(phi2)              
        n=(m1**2-m2**2)/(q2-q1)
        C=m1**2 +n*q1
        p, p0 =(elipsoid *(C -n*q)**0.5)/n,elipsoid *((C-n*q0)**0.5)/n 
        theta = n*(lda- lda0)        
        x,y = p*sin(theta),p0-p*cos(theta)
        return x,y  
        
 '''
