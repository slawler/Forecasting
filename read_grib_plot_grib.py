# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 11:09:45 2016

@author: slawler
"""
import pygrib
import numpy as np
import pandas as pd
from glob import glob
import matplotlib.pyplot as plt

files = glob('*.grb')

for f in files:
    gribfile = f
    grbs = pygrib.open(gribfile)
    
    print gribfile
    
    for grb in grbs:
          print grb
          
    grb_vals  = pd.DataFrame(grb.values[:])
    
    grbs.close()
    
    fig = plt.figure(figsize=(7,5))
    
    ax = fig.add_subplot(111)
    ax.set_title('%s' %str(f))
    plt.imshow(grb_vals)
    ax.set_aspect('equal')
    
    cax = fig.add_axes([0.12, 0.1, 0.78, 0.8])
    cax.get_xaxis().set_visible(False)
    cax.get_yaxis().set_visible(False)
    cax.patch.set_alpha(0)
    cax.set_frame_on(False)
    plt.colorbar(orientation='vertical')
    
    plt.savefig('/home/slawler/Desktop/20160224/12/figures/%s.png' %str(gribfile[:-5]))
    plt.close()
  