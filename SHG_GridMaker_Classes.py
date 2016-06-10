
from netCDF4 import Dataset
from pyproj import Proj
from numpy import floor as flr
from numpy import array


class Grid(object):
   
    def __init__(self, grid):
        self.grid = grid
        
    def dec_lats(self):   
        f = Dataset(self.grid,'r')
        lats   = f.variables['Latitude'][:]
        return lats
    
    def dec_lons(self):   
        f = Dataset(self.grid,'r')
        lons   = f.variables['Longitude'][:]
        return lons
        
    def LowerLeft_LatLon(self): 
        lats, lons  = self.dec_lats(), self.dec_lons()
        xmin,ymin = min(lons), min(lats)
        return xmin, ymin
              
    def proj_shift(self,i,j):
        proj = Proj('+proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=23.0 + \
                 lon_0=-96 +x_0=0 + y_0=0+ellps=GRS80 +datum=NAD83 + \
                 units=m +no_defs ')
        x, y  = proj(i,j)         
        return x,y        
        
    def DecDeg2SHG(self,i,j):
        x, y  = self.proj_shift(i,j)
        grid_x, grid_y  = int(flr(x)/250),int(flr(1)/250)  
        return grid_x, grid_y  
 
    def columns(self): 
        cols= []
        lats, lons  = self.dec_lats(), self.dec_lons()
        for x in lons:
            colname = self.DecDeg2SHG(x,lats[0])
            cols.append(colname[0])
        return array(cols)
    
    def rows(self): 
        rows = []
        lats, lons  = self.dec_lats(), self.dec_lons()
        for y in lats:
            rowname = self.DecDeg2SHG(lons[0],y)
            rows.append(rowname[0])
        return array(rows)
