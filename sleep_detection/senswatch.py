# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 17:58:36 2018

@author: lsxhcb
"""

from __future__ import division, print_function, absolute_import
# from numpy import __version__ as __numpy_version__ 
import time as tm
import re
import numpy as np


class Steam(object):
    """
    summary of class here
    
    Attrbutes:
        steam: one piece of data.
    """
    
    def __init__(self, steam):
        """ get attribute steam """
        self.steam = steam
    
    def _check_steam(self):
        """determine if the data format is correct
        
        Returns: 
            True or False.
        """
        steam = self.steam
        return re.match('^[a-zA-Z0-9]{13};\[[a-zA-Z0-9\,\s+]+\]', steam) != None
    
    def _steam2lst(self):
        """transform the steam to a list
        
        Returns:
            A list contains two items. For example:
                
            [1542792011307, [171, 0, 17, 255, 161, 74, 235, 21, 194, 0, 0, 75, 1,
            0, 225, 1, 0, 78, 4, 203]]   
        """
        
        steam = self.steam
        steam = str(steam)
        lst = steam.split(';')
        lst[0] = int(lst[0])
        lst[1] = lst[1].replace('[','').replace(']','')
        lst[1] = lst[1].split(',')
        lst[1] = list(map(lambda i: int(i), lst[1]))
        return lst

    def _parse(self):
        """parse the input data
        
        Returns:
            A dict contains the information of raw data. For example:
            
            if the frameLen == 7:
                frame = {'time':1542792011477, 'hr':87} 
            if the frameLen == 20:
                frame = {'time':1542792011307, 'ppg':1564, 'acc1':46, 'acc2':153, 'acc3':18}
            else:
                frame = {'error':[1542792011307, [0, 0, 1]], 'line':1}
        """
        
        steam = self.steam
        steam = self._steam2lst()
        frameLen = len(steam[1])                    
        if frameLen == 20:
            frame = FrameRaw()
            frame.frame = frame._parse(steam)        # frame.flag=True;  frame.type='raw'
#            if frame.flag:                          # frame.flag=True; 
#                frame.frame = frame
#            else:
#                frame = FrameDrop()._parse(steam)   # frame.flag=False; frame.type='drop'
#                frame.frame = frame
        elif frameLen == 7:
            frame = FrameConv()
            frame.frame = frame._parse(steam)        # frame.flag=True;  frame.type='conv'
        else:
            frame = FrameDrop()
            frame.frame = frame._parse(steam)        # frame.flag=False; frame.type='drop'
        return frame    
        
    def parse(self):
                
        steam = self.steam
        if self._check_steam():
            steam = self._steam2lst()
            frame = self._parse()
        elif not steam:
            frame = FrameDrop()
            frame.frame = frame._parse(steam)
        else:
            frame = np.inf
            frame = FrameDrop()
            frame.frame = frame._parse(steam)
        return frame

  
class BaseFrame(object):
    
    def __init__(self):
#        self.frame = frame
#        self.time_loc = 0
#        self.vals_loc = 1
        self.protocol = None
        self.type = None
        self.flag = None
    
#    @property
#    def frame(self):
#        return None    
    
    @property
    def time_loc(self):
        """the date of input data always in position1, so return 0"""
        return 0
    
    @property
    def vals_loc(self):
        """the value of input data always in position2, so return 1"""
        return 1    
    
    def _parse_time_func(self, time):
#        frame = self.frame
#        time = frame[self.time_loc]
#        time = [time]
        return time
    
    def _prase_date_func(self, date, date0_loc, date1_loc, date2_loc, date3_loc):
        frame = self.frame
        date0 = '{:08b}'.format(frame[date0_loc]) 
        date1 = '{:08b}'.format(frame[date1_loc])
        date2 = '{:08b}'.format(frame[date2_loc])
        date3 = '{:08b}'.format(frame[date3_loc])
        date = (date0+date1+date2+date3)[::-1]
        date_sec  = int(date[0 : 5], 2)
        date_min  = int(date[6 :11], 2)
        date_hour = int(date[12:16], 2)
        date_day  = int(date[17:21], 2)
        date_mon  = int(date[22:25], 2)
        date_year = int(date[26:31], 2) + 2000
        time = tm.struct_time(
                tm_year=date_year, 
                tm_mon =date_mon, 
                tm_mday=date_day, 
                tm_hour=date_hour, 
                tm_min =date_min, 
                tm_sec =date_sec)
        return time
        
    def _parse_vals_func(self, vals):
        """A abstract function, implemented by subclasses."""
        pass
    
    def _parse(self, frame):
        """A abstract function, implemented by subclasses."""
        pass


class FrameConv(BaseFrame):
    """sub class of BaseFrame, get the heart value"""
    
    def __init__(self):
        super(FrameConv, self).__init__()
#        self.time_loc = 0
#        self.vals_loc = 1
        self.protocol = {'hr_loc': 6}
        self.type = 'conv'
        self.flag = True
    
    def _parse_vals_func(self, vals):
        super(FrameConv, self)._parse_vals_func(vals)
        val_loc = self.protocol['hr_loc']    # get the accordinate of heart value.
#        value = list() 
#        value.append(vals[val_loc])
        value = vals[val_loc]    # get the heart value
        return value 
    
    def _parse(self, frame):
        super(FrameConv, self)._parse(frame)
#        frame = self.frame
        time = frame[self.time_loc]
        vals = frame[self.vals_loc]
        parse_time = self._parse_time_func(time)
        parse_vals = self._parse_vals_func(vals)
        prase_frame = {'time':parse_time, 
                       'hr'  :parse_vals}
        return prase_frame


class FrameRaw(BaseFrame):
    """sub class of BaseFrame, get the ppg and acceleration value"""
    
    def __init__(self):
        super(FrameRaw, self).__init__()
#        self.frame = frame
#        self.time_loc = 0
#        self.vals_loc = 1
        self.protocol = {
        'date3_loc': 5,
        'date2_loc': 6,
        'date1_loc': 7,
        'date0_loc': 8,
        'xSign_loc': 9,
        'xHigh_loc': 10,
        'xLow_loc' : 11,
        'ySign_loc': 12,
        'yHigh_loc': 13,
        'yLow_loc' : 14,        
        'zSign_loc': 15,
        'zHigh_loc': 16,
        'zLow_loc' : 17,
        'pHigh_loc': 18,
        'pLow_loc' : 19}
        self.type = 'raw'
        self.flag = True
    
    def _parse_vals_func(self, vals):
        
        def _prase_acc_func(vals, sign_loc, high_loc, low_loc):
            """ Get the acceleration value according to the 
                formulation: sign * (high*256 + low)
            """
            
            sign = vals[sign_loc]
            high = vals[high_loc]
            low  = vals[low_loc]
            if sign == 0:
                sign = -1
                value = sign * (high*256+low)
            elif sign == 1:
                sign = 1
                value = sign * (high*256+low)
            else:
#                self.flag = False
                value = None
            return value
        
        def _prase_ppg_func(vlas, high_loc, low_loc):
            """ Get the ppg value according to the
                formulation: high*256 + low
            """    
            
            high = vals[high_loc]
            low  = vals[low_loc]
            value = high * 256 + low
            return value
        
        xSign_loc = self.protocol['xSign_loc']
        xHigh_loc = self.protocol['xHigh_loc']
        xLow_loc  = self.protocol['xLow_loc']
        ySign_loc = self.protocol['ySign_loc']
        yHigh_loc = self.protocol['yHigh_loc']
        yLow_loc  = self.protocol['yLow_loc']
        zSign_loc = self.protocol['zSign_loc']
        zHigh_loc = self.protocol['zHigh_loc']
        zLow_loc  = self.protocol['zLow_loc']
        pHigh_loc = self.protocol['pHigh_loc']
        pLow_loc  = self.protocol['pLow_loc']
        value = list()   # contains ppg and triaxial acceleration values
        value.append(_prase_ppg_func(vals, pHigh_loc, pLow_loc))
        value.append(_prase_acc_func(vals, xSign_loc, xHigh_loc, xLow_loc))        
        value.append(_prase_acc_func(vals, ySign_loc, yHigh_loc, yLow_loc))
        value.append(_prase_acc_func(vals, zSign_loc, zHigh_loc, zLow_loc))
        return value
        
    def _parse(self, frame):
        super(FrameRaw, self)._parse(frame)
#        frame = self.frame
        
        time = frame[self.time_loc]
        vals = frame[self.vals_loc]
        parse_time = self._parse_time_func(time)
        parse_vals = self._parse_vals_func(vals)        
        prase_frame = {'time': parse_time,
                       'ppg ': parse_vals[0],
                       'acc1': parse_vals[1],
                       'acc2': parse_vals[2],
                       'acc3': parse_vals[3]}
        return prase_frame

    
class FrameDrop(BaseFrame):
    """sub class of BaseFrame, get the information of irrational data"""
    
    def __init__(self):
        super(FrameDrop, self).__init__()
        self.flag = False
    
#    def _parse_time_func(self):
#        super(FrameDrop, self)._parse_time_func()
#        time = [None]
#        return time

#    def _parse_vals_func(self):
#        super(FrameDrop, self)._parse_vals_func()
#        value = [None]
#        return value
    
    def _parse(self, frame):
        super(FrameDrop, self)._parse(frame)
        parse_frame = {'error': frame}
        return parse_frame


def parser(path, mertic='sec'):
    """Over all analytic function.
    
    Args:
        path: path of the file.
    
    Returns:
        raw:  a list contains many dicts which contain date,ppg and acceleration values.  
        conv: a list contains many dicts which contain date and heart value.    
        drop: a list contains many dicts which contain the irrational data.  
    """
    
    file = open(file=path, mode='rt', encoding='utf-8')
#    with open(file=path, mode='rt', encoding='utf-8') as file:
    conv = list()
    raw  = list()
    drop = list()
    for line, steam in enumerate(file):
        steam = str(steam)
        frame = Steam(steam).parse()
        if frame.type == 'conv':
            conv.append(frame.frame)
        elif frame.type == 'raw':
            raw.append(frame.frame)
        else:
            frame.frame['line'] = line
            drop.append(frame.frame)
    file.close()
    print(path)
    return raw, conv, drop    

