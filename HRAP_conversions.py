# -*- coding: utf-8 -*-
"""
Created on Sat Feb 27 21:58:52 2016

Converted from fortran code:
http://www.nws.noaa.gov/oh/hrl/dmip/lat_lon.txt

@author: slawler
"""

#subroutine converts lat-lon to HRAP
# rlon   - longitude in fractional degrees
# rlat   - lattitude in fractional degrees

# output variables
#hrap_x - global HRAP x-coordinate
#hrap_y - global HRAP y-coordinate

def latlon_to_hrap(rlon,rlat):
    pi=3.141592654
    d2rad, earthr =pi/180., 6371.2
    ref_lat, ref_lon =60., 105.
    rmesh=4.7625
    tlat=ref_lat*d2rad
    re=(earthr*(1.+np.sin(tlat)))/rmesh
    flat=rlat*d2rad
    flon=(rlon+180.-ref_lon)*d2rad
    r=re*np.cos(flat)/(1.+np.sin(flat))
    x=r*np.sin(flon)
    y=r*np.cos(flon)
    hrap_x=x+401.
    hrap_y=y+1601.
    return np.round(hrap_x,0),np.round(hrap_y,0)
    
latlon_to_hrap(77.693,38.591)

#===Not Converted
#c**********************************************************************
#      subroutine hrap_to_latlon(hrap_x,hrap_y,rlon,rlat)
#c**********************************************************************
#c
#c subroutine converts HRAP to lat-lon
#c
#c input variables
#c
#c hrap_x - global HRAP x-coordinate
#c hrap_y - global HRAP y-coordinate
#c
#c output variables
#c
#c rlon   - longitude in fractional degrees
#c rlat   - lattitude in fractional degrees
#c
#      earthr=6371.2
#      stlon=105.
#      pi=3.141592654
#      raddeg=180./pi
#      xmesh=4.7625
#      tlat=60./raddeg
#      x=hrap_x-401.
#      y=hrap_y-1601.
#      rr=x*x+y*y
#      gi=((earthr*(1.+sin(tlat)))/xmesh)
#      gi=gi*gi
#      rlat=asin((gi-rr)/(gi+rr))*raddeg
#      ang=atan2(y,x)*raddeg
#      if(ang.lt.0.) ang=ang+360.
#      rlon=270.+stlon-ang
#      if(rlon.lt.0.) rlon=rlon+360.
#      if(rlon.gt.360.) rlon=rlon-360.
#      return
#      end