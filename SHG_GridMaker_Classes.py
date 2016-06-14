from netCDF4 import Dataset
from numpy import floor as flr
from numpy import array,arange, meshgrid
from scipy import interpolate as intp
from numpy import pi,sin,cos,log

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
        
    def precip(self):   
        f = Dataset(self.grid,'r')
        precip  = f.variables['rain_10min'][:]
        return precip    
        
    def ll_latlon(self): 
        lons, lats  = self.dec_lons(),self.dec_lats()
        xmin,ymin = min(lons), min(lats)
        return xmin, ymin
              
    def ur_latlon(self): 
        lons, lats  = self.dec_lons(),self.dec_lats()
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
        q,q0 ,q1,q2= q_fun(phi),q_fun(phi0),q_fun(phi1),q_fun(phi2)              
        n=(m1**2-m2**2)/(q2-q1)
        C=m1**2 +n*q1
        p, p0 =(elipsoid *(C -n*q)**0.5)/n,elipsoid *((C-n*q0)**0.5)/n 
        theta = n*(lda- lda0)        
        proj_x,proj_y = p*sin(theta),p0-p*cos(theta)
        return proj_x,proj_y  
    
    
    def DecDeg2SHG(self,i,j):
        x, y  = self.ToAlbers(i,j)
        grid_x, grid_y  = int(flr(x)/self.cellsize),int(flr(y)/self.cellsize)  
        return grid_x, grid_y  

    def ll_SHG(self): 
        ll_x,ll_y = self.ll_latlon()
        shg_ll_x, shg_ll_y = self.DecDeg2SHG(ll_x,ll_y)
        return shg_ll_x, shg_ll_y  
              
    def flat_dims(self):
        lons0,lats0 = meshgrid(self.dec_lons(),self.dec_lats()) 
        lons,lats= (lons0.flatten(),lats0.flatten())
        return lons,lats
    
    def flat_grd(self): 
        p = self.precip().flatten()
        return p
        
    def ReGrid(self, xmin, ymin, xmax, ymax):
        lons0,lats0  = self.flat_dims()[0],self.flat_dims()[1]       
        lons1,lats1 = meshgrid(arange(xmin,xmax,0.002),arange(ymin,ymax,0.002))
        precip_clp = intp.griddata((lons0,lats0),self.flat_grd(),(lons1, lats1), method='linear')
        return precip_clp
    
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
        
        
        
nfile = '29May2015_071200_10min.nc'
g= Grid(nfile,500)           
coords = -96.9635,32.6258,-96.2579,33.1449
