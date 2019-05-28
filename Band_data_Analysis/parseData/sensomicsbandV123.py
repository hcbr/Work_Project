# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 17:58:36 2018

@author: lsx
"""



import pandas as pd
import datetime as dt
import re


class BaseFrame(object):
    
    def __init__(self, frame):
        self.frame = frame
        self.time_loc = 0
        self.vals_loc = 1
        self.time = None
        self.vals = None
        self.protocol = None
        self.type = None
        self.flag = None
    
    def _prase_time(self, trans=True):
        
        frame = self.frame
        time = frame[self.time_loc]
        if trans: # trans to sec (str type)
#            time = dt.datetime.fromtimestamp(time/1000).strftime('%Y-%m-%d %H:%M:%S')
            time = dt.datetime.fromtimestamp(time/1000).strftime('%Y-%m-%d %H:%M:%S.%f')
        time = [time]
        self.time = time
        return time
    
    def _prase_value(self):
        pass

    def _check_data(self):
        pass
  
    
           
class FrameParse(BaseFrame):
    
    def __init__(self, frame):
        super(FrameParse, self).__init__(frame)
        self.frame = frame
        self.time_loc = 0
        self.vals_loc = 1
        self.time = None
        self.vals = None
        self.protocol = {'hr_loc': 6}
        self.type = 'parse'
        self.flag = True
        
    def _prase_value(self):
        super(FrameParse, self)._prase_value()
        frame = self.frame
        vals = frame[self.vals_loc]
        value = list()
        hr_loc = self.protocol['hr_loc']
        value.append(vals[hr_loc])
        self.vals = value
        return value
 
    
    
class FrameRaw(BaseFrame):
    
    def __init__(self, frame):
        super(FrameRaw, self).__init__(frame)
        self.frame = frame
        self.time_loc = 0
        self.vals_loc = 1
        self.time = None
        self.vals = None
        self.protocol = {
        'date3_loc': 5,
        'date2_loc': 6,
        'date1_loc': 7,
        'date0_loc': 8,
        'xSign_loc': 9,
        'xHigh_loc': 10,
        'xLow_loc':  11,
        'ySign_loc': 12,
        'yHigh_loc': 13,
        'yLow_loc':  14,        
        'zSign_loc': 15,
        'zHigh_loc': 16,
        'zLow_loc':  17,
        'pHigh_loc': 18,
        'pLow_loc':  19        
        }
        self.type = 'raw'
        self.flag = True

    def _prase_acc_func(self, frame, sign_loc, high_loc, low_loc):
        """
            formulation: symbol * (high*256 + low)
        """
        symb = frame[sign_loc]
        high = frame[high_loc]
        low = frame[low_loc]
        if symb == 0:
            sign = -1
            value = sign*(high*256+low)
        elif symb == 1:
            sign = 1
            value = sign*(high*256+low)
        else:
            value = [None]
        return value
    
    def _prase_ppg_func(self, frame, high_loc, low_loc):
        """
            formulation: high*256 + low
        """        
        high = frame[high_loc]
        low = frame[low_loc]
        value = high*256+low
        return value
    
    def _prase_date_func(self, frame, date0_loc, date1_loc, date2_loc, date3_loc):
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
        pass
              
# =============================================================================
# a = 72
# b = 70
# c = 205
# d = 230
# dd = '{:08b}'.format(d)
# #dd = dd[::-1]
# cc = '{:08b}'.format(c)
# #cc = cc[::-1]
# bb = '{:08b}'.format(b)
# #bb = bb[::-1]
# aa = '{:08b}'.format(a)
# #aa = aa[::-1]
# #e = dd+cc+bb+aa
# e = aa+bb+cc+dd
# e = e[::-1]
# date_sec  = int(e[0 : 6], 2)
# date_min  = int(e[6 :12], 2)
# date_hour = int(e[12:17], 2)
# date_day  = int(e[17:22], 2)
# date_mon  = int(e[22:26], 2)
# date_year = int(e[26:32], 2) + 2000
# 
# =============================================================================
            
    def _prase_value(self):
        super(FrameRaw, self)._prase_value()
        frame = self.frame
        vals = frame[self.vals_loc]
        value_acc = list()
        value_ppg = list()
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
        value_acc.append(self._prase_acc_func(vals, xSign_loc, xHigh_loc, xLow_loc))
        value_acc.append(self._prase_acc_func(vals, ySign_loc, yHigh_loc, yLow_loc))
        value_acc.append(self._prase_acc_func(vals, zSign_loc, zHigh_loc, zLow_loc))
        value_ppg.append(self._prase_ppg_func(vals, pHigh_loc, pLow_loc))
        value = value_acc + value_ppg
        self.vals = value
        return value
    
class FrameDrop(BaseFrame):
    
    def __init__(self, frame):
        super(FrameDrop, self).__init__(frame)
        if not frame:
            self.frame = frame
        else:
            self.frame = None
        self.flag = False
        
    def _prase_time(self):
        super(FrameDrop, self)._prase_time()
        pass
        
    def _prase_value(self):
        super(FrameDrop, self)._prase_value()
        pass
    


class Steam(object):
    
    def __init__(self, steam):
        self.steam = steam
        self.column_time = 'time'
        self.column_vals = 'value'
    
    def _check_steam(self):
        steam = self.steam
        return re.match('^[a-zA-Z0-9]{13};\[[a-zA-Z0-9\,\s+]+\]', steam) != None
                
    def prase(self):
        
        def _steam2lst(steam):
            steam = str(steam)
            lst = steam.split(';')
            lst[0] = int(lst[0])
            lst[1] = lst[1].replace('[','').replace(']','')
            lst[1] = lst[1].split(',')
            lst[1] = list(map(lambda i: int(i), lst[1]))
            return lst
        
        steam = self.steam
        if self._check_steam():
            steam = _steam2lst(steam)        
            frameLen = len(steam[1])                     
            if frameLen == 7:
                frame = FrameParse(steam) # frame.type='parse'; frame.flag=True
                time = frame._prase_time()
                vals = frame._prase_value()
                frame.frame = time+vals
            elif frameLen == 20:
                frame = FrameRaw(steam)   # frame.type='raw';   frame.flag=True
                time = frame._prase_time()
                vals = frame._prase_value()
                frame.frame = time+vals
            else:
                frame = FrameDrop(steam)  # frame.flag=False
                frame.frame = steam
        else:
            frame = FrameDrop(steam)  # frame.flag=False
            frame.frame = steam
            
        return frame
    


class BaseData(object):
    
    def __init__(self, data):
        self.data = pd.DataFrame(data)
        self.cols = ['time', 'value']
        self.dtype = None
    
    def to_datetime(self, mertic='mic', save=True, path=None):

        def tans2sec(t):
            t = dt.datetime(t.year, t.month, t.day, t.hour, t.minute, t.second)
            return t
        
        def tans2min(t):
            t = dt.datetime(t.year, t.month, t.day, t.hour, t.minute, 0)
            return t
        
        cols = self.cols
        data = self.data.copy()
        data[cols[0]] = pd.to_datetime(data[cols[0]]) # str 2 datetime
        
        if mertic == 'mic':
            #data = data.groupby(cols[0])[cols[1:]] # groupby
            #data = list(data)
#            data = data.groupby('time')
#            data = data.reset_index(drop=True)
            data = data
        elif mertic == 'sec':
            data[cols[0]] = data[cols[0]].apply(lambda t: tans2sec(t))
            data = data.groupby(cols[0])[cols[1:]].median() # groupby
            ## reindex
            tidx = list(data.index) 
            stime = tidx[0]
            etime = tidx[-1]
            ridx = list(pd.date_range(stime, etime, freq='s'))
            data = data.reindex(index=ridx)
            data = data.fillna(method='pad')
            data = data.reset_index()
        elif mertic == 'min':
            data[cols[0]] = data[cols[0]].apply(lambda t: tans2min(t)) # sec 2 min
            data = data.groupby(cols[0])[cols[1:]].median() # groupby
            data = data.reset_index()            
        else:
            raise ValueError
            
        if save:
            out = data.copy()
            out[cols[0]] = out[cols[0]].apply(lambda t: str(t))        
            out = data.to_json(orient='records')
            with open(path, 'w') as f:
                f.write(out)        
        return data            
        
    def to_difftime(self, mertic='mic', save=True, path=None):
    
        def diff_mictime(t, t0):
            d = t - t0
            d = d.total_seconds()
            d = d*1000
            return d
        
        def diff_sectime(t, t0):
            d = t - t0
            d = d.total_seconds()
            d = int(d)
            return d
        
        def diff_mintime(t, t0):
            d = t- t0
            d = d.total_seconds()
            d = int(int(d)/60)
            return d
        
        cols = self.cols
        data = self.data.copy()
        data[cols[0]] = pd.to_datetime(data[cols[0]]) # str 2 datetime
        t0 = data.loc[0, cols[0]]
        
        if mertic == 'mic':
            data[cols[0]] = data[cols[0]].apply(lambda t: diff_mictime(t, t0))
        elif mertic == 'sec':
            data[cols[0]] = data[cols[0]].apply(lambda t: diff_sectime(t, t0))
        elif mertic == 'min':
            data[cols[0]] = data[cols[0]].apply(lambda t: diff_mintime(t, t0))
        else:
            raise ValueError
            
        if save:
            out = data.copy()
            out[cols[0]] = out[cols[0]].apply(lambda t: str(t))        
            out = data.to_json(orient='records')
            with open(path, 'w') as f:
                f.write(out)
        return data
    


class DataParse(BaseData):
    
    def __init__(self, data):
        super(DataParse, self).__init__(data)
        self.cols = ['time', 'hr']
        self.data = pd.DataFrame(data, columns=self.cols)
        
        

class DataRaw(BaseData):
    
    def __init__(self, data):
        super(DataRaw, self).__init__(data)
        self.cols = ['time', 'ac1','ac2','ac3','ppg']
        self.data = pd.DataFrame(data, columns=self.cols)
 
    

class DataError(object):
    
    def __init__(self, data):
        self.cols = ['file', 'value']
        self.data = data
        
    def to_record(self, save=False, path=None):
        return self.data



def parser(path, mertic='sec'):
    file = open(file=path, mode='rt', encoding='utf-8')
    parse = list()
    raw = list()
    error = list()
    for steam in file:
        steam = str(steam)
        frame = Steam(steam).prase()
        if frame.flag:
            if frame.type == 'parse':
                parse.append(frame.frame)
            elif frame.type == 'raw':
                raw.append(frame.frame)
            else:
                pass
        else:
            error.append([path, frame.frame])
    
    dataraw = DataRaw(raw)
    dataparse = DataParse(parse)
    dataerror = DataError(error)
    raw = dataraw.to_datetime(mertic=mertic,save=False)
    parse = dataparse.to_datetime(mertic=mertic,save=False)
    error = dataerror.to_record(save=False)
    return raw, parse, error