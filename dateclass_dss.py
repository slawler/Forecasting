# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 21:05:35 2016
@author: slawler
"""

from datetime import datetime, timedelta
from re import findall
from ast import literal_eval

class dssWriter:

    def __init__(self, name):
        self.name = name

    def date(self):
        f = self.name.split('_')
        date = datetime.strptime(f[0]+f[1],'%d%b%Y%H%M%S')
        return date

    def dss_start(self):
        dss_start = self.date().strftime('%d%b%Y:%H%M')
        return dss_start

    def delta_t(self):
        f = self.name.split('_')
        interval = findall('\d+|\D+', str(f[2][:-3]))
        scalar, unit = interval[0], interval[1]

        if unit == 'min.':
            unit = 'minutes'
        elif unit == 'hour':
            unit = 'hours'

        params = "{'%s': %s}" %(unit, scalar)
        delta_t = timedelta(**literal_eval(params))
        return delta_t

    def dss_stop(self):
        stop = self.date() + self.delta_t()

        if stop.hour == 00:
            dss_stop = stop.strftime('%d%b%Y:%H%M')[:10] + '2400'
        else:
            dss_stop = stop.strftime('%d%b%Y:%H%M')
        return dss_stop

    def dss_string(self):
        command      = 'asc2dssGrid.exe in='
        dss          = ' dss='
        DSSNAME      = self.date().strftime('%b%Y')+'.dss'
        path         = ' path='
        info         = '/SHG/CASA/PRECIP/%s/%s/Import'%(self.dss_start(),self.dss_stop())
        #nextline     = '\n'
        dss_string = command + self.name + dss + DSSNAME + path +info #+ nextline
        return dss_string
        
        
a = dssWriter(nfile)       
