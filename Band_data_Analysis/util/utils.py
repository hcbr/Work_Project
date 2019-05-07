# -*- coding: utf-8 -*-

import pandas as pd
import datetime as dt


def tans2min(t):
    t = dt.datetime(t.year, t.month, t.day, t.hour, t.minute, 0)
    return t


def combine(hrs, hrf, sc = 'time'):
    hrsf = pd.merge(hrs, hrf, on = sc)
    hrsf['time'] = hrsf['time'].apply(lambda x: tans2min(x))
    hrsf = hrsf.groupby(['time']).mean()
    hrsf = hrsf.reset_index()
    return hrsf


def miss_value(f_data, count):
    miss_all = []
    for i in range(len(f_data)-1):
        miss = int((f_data['time'][i+1] - f_data['time'][i]).seconds)
        if miss < 60:
            miss_all.append((miss)-1)
        else:
            miss_all.append(count)
    return miss_all


def padding(f_data, count=10):
    f_miss = miss_value(f_data, count)
    hrf = pd.DataFrame()
    hr =  f_data.iloc[:,1]
    for i in range(len(hr)-1):
        pad_value = pd.DataFrame([None]*f_miss[i])
        tmp = pd.concat([pd.DataFrame([hr[i]]),pad_value],axis=0)
        hrf = pd.concat([hrf,tmp],axis=0)
    hrf = pd.concat([hrf,pd.DataFrame([hr[len(hr)-1]])])
    hrf.columns = ['hr'] 
    hrf = hrf.reset_index(drop=True)
    return hrf


def padding_gnd(gnd, bias):
    inter = pd.DataFrame([None]*59) 
    hrg = pd.DataFrame()
    for hrg_i in gnd:
        tmp = pd.concat([pd.DataFrame([hrg_i]),inter], axis=0)
        hrg = pd.concat([hrg, tmp], axis=0)
    hrg = hrg.reset_index(drop=True)
    inter2 = pd.DataFrame([None]*bias)
    hrg = pd.concat([inter2,hrg], axis=0)
    hrg = hrg.reset_index(drop=True)
    return hrg