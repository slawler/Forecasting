
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
