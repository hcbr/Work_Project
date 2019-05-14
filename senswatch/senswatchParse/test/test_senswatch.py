#!/usr/bin/env pypy
# -*- coding: utf-8 -*-
#
# (c) Sixing Liu, Changbin Huang <sixingliu@sensomics.com> 2019
# MIT licence (i.e. almost public domain)
# 'Programming Language :: Python 3.6'
# 'Operating System :: OS Independent'
  

import sys
sys.path.append("..")

import datetime as dt
import pandas as pd
import senswatch


def tans2sec(timeStamp):
    """change the format of datatime."""
    timeArray = dt.datetime.fromtimestamp(timeStamp/1000).strftime('%Y-%m-%d %H:%M:%S')
    return timeArray


def getDataframe():
    """A test of parsing txt file to DataFrame format
    
    senswatch.parser function:
    Over all function.
    
    Args:
        path: path of the file.
    
    Returns:
        raw:  a list contains dicts consist of   
            time: int, Unix timestamp  
            ppg : int, Photoplethysmography values   
            acc1: int, Acceleration in x axis;  
            acc2: int, Acceleration in y axis;  
            acc3: int, Acceleration in z axis;  
        conv: a list contains dicts consist of   
            time: int, Unix timestamp;  
            hr  : int, Heart rate  
        drop: a list contains dicts consist of the irrational data.  
    """
    
    filepath = 'sens_test_data.txt'
    raw, conv, drop = senswatch.parser(filepath)
    
    raw = pd.DataFrame(raw)
    conv = pd.DataFrame(conv)
    drop = pd.DataFrame(drop)
    print(raw.head(n=5))
    print(conv.head(n=5))
    print(drop.head(n=5))
    
#    '''
#    An Example of transforming timestramp to date type
#    '''
    raw_ = raw.copy()
    raw_['time'] = raw['time'].apply(lambda t: tans2sec(t))
    print(raw_.head(n=5))

if __name__ == '__main__':
    getDataframe()