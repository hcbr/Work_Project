
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 20:43:06 2019

@author: hcb
"""

import os
import parseData.microband
import parseData.sensomicsbandV123 as sob
import pandas as pd
import datetime as dt
from Analysis_Function.analysis import Correlation
from util.utils import combine, padding, padding_gnd
import matplotlib.pyplot as plt
from Plot_Function.plot_bar import plotpicture


"""Man:"""

'''select suitable data'''

## sensomics data

filepath = './data/sens/3-14-1'
filelist = os.listdir(filepath)
hrs = pd.DataFrame()
raw = pd.DataFrame()
for file in filelist[0:37]:
    print(file)
    path = os.path.join(filepath, file)
    #tmp, temp, error = sob.parser(path, mertic='sec')
    tmp, temp, error = sob.parser(path, mertic='sec')
    hrs = pd.concat([hrs, temp])
    raw = pd.concat([raw, tmp])
hrs = hrs.reset_index(drop=True)
# data of still (position1)
hrsstill = hrs[0:937]
hrsstill = hrsstill.reset_index(drop=True)
# data of work (position2)
hrswork = hrs[2094:3034]
hrswork = hrswork.reset_index(drop=True)

# divide into three groups
hrs1 = pd.concat([hrsstill[0:294], hrswork[0:295]], axis=0)
hrs1 = hrs1.reset_index(drop=True)
hrs2 = pd.concat([hrsstill[294:584], hrswork[295:592]], axis=0)
hrs2 = hrs2.reset_index(drop=True)
hrs3 = pd.concat([hrsstill[584:877], hrswork[592:880]], axis=0)
hrs3 = hrs3.reset_index(drop=True)


## fitbit data (man)

path = './data/Fibit'
filelist = os.listdir(path)
path1 = os.path.join(path, filelist[2]) 
path2 = os.path.join(path, filelist[3])
# position1
hrfstill = pd.read_excel(path1,names=['time','heart'])
hrfstill = hrfstill.sort_values('time')
hrfstill = hrfstill.reset_index(drop=True)
# position2
hrfwork = pd.read_excel(path2,names=['time','heart'])
hrfwork = hrfwork.sort_values('time')
hrfwork = hrfwork.reset_index(drop=True)
# divide into three groups
hrf1 = pd.concat([hrfstill[0:43], hrfwork[0:45]], axis=0)
hrf1 = hrf1.reset_index(drop=True)
hrf2 = pd.concat([hrfstill[43:74], hrfwork[45:91]], axis=0)
hrf2 = hrf2.reset_index(drop=True)
hrf3 = pd.concat([hrfstill[74:113], hrfwork[91:134]], axis=0)
hrf3 = hrf3.reset_index(drop=True)


## merge hrs and hrf by 'time'
info1 = combine(hrs1, hrf1)  # first group
info2 = combine(hrs2, hrf2)
info3 = combine(hrs3, hrf3)
info = pd.concat([info1, info2, info3])

# label of each group (after combine)
gnd1 = [63,61,64,64,65,63,61,62,61,61]
gnd2 = [66,64,67,66,67,62,64,64,63,65]
gnd3 = [65,69,66,64,69,61,62,70,63,65]


'''analysis'''

## get correlation coefficient and mse
# about hrs
corf = Correlation(info1['heart'], gnd1)
f_corre, f_mse = corf.getresult()
# about hrf
cors = Correlation(info1['hr'], gnd1)
s_corre, s_mse = corf.getresult()
# pear_s = cors.pearson()

"""plot picture"""
pltt = plotpicture() 

'''plot the picture about mean fitting of each group and all data'''

y1 = info1['hr']
y2 = info1['heart']
gnd1 = [63,61,64,64,65,63,61,62,61,61]
pltt.mean_fitting(y1, y2, gnd1, ylim=[55,75])

'''get the mse value of three groups plot the histogram'''
y1 = [0.676,2.32,1.63]
y2 = [1.24,2.89,5.09]
pltt = plotpicture()
pltt.bar(y1, y2, xlabel='Experiment sets',ylabel='Mse',ylim=[0,7],title="Regression correlation",save=False)

'''get the correlation value of three groups and plot the histogram'''
y1 = [0.906,0.784,0.908]
y2 = [0.874,0.843,0.707]
pltt.bar(y1, y2, xlabel='Experiment sets',ylabel='Correlation coefficient',ylim=[0,1.4],title="Spearman's rank  correlation coefficient",save=False)

'''plot the sequentially according to time'''
 
# align the start time
hrf3 = hrf3[5:]
hrf3 = hrf3.reset_index(drop=True)
hrs3 = hrs3[3:]
hrs3 = hrs3.reset_index(drop=True)

# supplement the data (mainly target on fitbit)
hrf33 = padding(hrf3, count=12)  #count:supplement the minute level interval  

hrs33 = padding(hrs3, count=8)

##用的6组标签
#gnd1 = [63,61,64,64,65,66,64,67,66,67,65,69,66,64,69]
#gnd1 = [63,61,64,64,65,63,61,62,61,61]
#gnd1 = [66,64,67,66,67,62,64,64,63,65]
#gnd1 = [65,69,66,64,69,61,62,70,63,65]
#gnd1 = [82,84,82,86,86,87,86,88,86,84] #29-33  #45-49
#gnd1 = [90,88,90,90,88,85,85,81,82,82] #34-38  #8-12
#gnd1 = [83,82,86,86,81,83,82,82.5,86,87.5] #40-44 #13-17

#supplement the gnd data
hrg = padding_gnd(gnd3, bias=20)

#plot
pltt.plot_sequentially(hrs33,hrf33,hrg,save=False)


'''prepare the data(man data) for distribution picture'''

## all data(each second)
man_hrs = pd.concat([hrsstill[0:877], hrswork[0:880]]) #combine two positions
man_hrs = man_hrs.reset_index(drop=True)
#suplement data
man_hrs = padding(man_hrs, count=4)
man_hrs = man_hrs.fillna(method='pad')
man_hrs = man_hrs.reset_index(drop=True)

man_hrf = pd.concat([hrfstill[0:113],hrfwork[0:134]])
man_hrf = man_hrf.reset_index(drop=True)
man_hrf = padding(man_hrf, count=20)
man_hrf = man_hrf.fillna(method='pad')
man_hrf = man_hrf.reset_index(drop=True)

#suplement the data to 30 minutes(1800s)
man_hrf = pd.concat([pd.DataFrame([67]*2,columns=['hr']), man_hrf],axis=0)
man_hrf = man_hrf.reset_index(drop=True)

man_hrs = pd.concat([pd.DataFrame([65]*1,columns=['hr']), man_hrs],axis=0)
man_hrs = man_hrs.reset_index(drop=True)


## mean data (each minute)

man_info = info


'''woman:'''

'''select suitable data'''

import os
import microband
import sensomicsbandV123 as sob
import pandas as pd
import datetime as dt
from analysis import Correlation

## sensomic data
filepath = './data/sens/2019-3-13'
filelist = os.listdir(filepath)
hrs = pd.DataFrame()
raw = pd.DataFrame()
for file in filelist[0:1]:
    print(file)
    path = os.path.join(filepath, file)
    #tmp, temp, error = sob.parser(path, mertic='sec')
    tmp, temp, error = sob.parser(path, mertic='sec')
    hrs = pd.concat([hrs, temp])
    #raw = pd.concat([raw, tmp])
hrs = hrs.reset_index(drop=True)
hrs['hr'] = hrs['hr'] + 9

filepath = './data/sens/2019-3-13-woman'
filelist = os.listdir(filepath)
hrswoman = pd.DataFrame()
rawwoman = pd.DataFrame()
for file in filelist[0:2]:
    print(file)
    path = os.path.join(filepath, file)
    #tmp, temp, error = sob.parser(path, mertic='sec')
    tmp, temp, error = sob.parser(path, mertic='sec')
    hrswoman = pd.concat([hrswoman, temp])
    #raw = pd.concat([raw, tmp])
hrswoman = hrswoman.reset_index(drop=True)

# two positions
hrswork = pd.concat([hrswoman[20:619], hrswoman[619:881]], axis=0)
hrswork = hrswork.reset_index(drop=True)
hrsstill = pd.concat([hrswoman[881:1181], hrs[0:600]])
hrsstill = hrsstill.reset_index(drop=True)

# divided into three groups
hrs1 = pd.concat([hrswork[0:300], hrsstill[0:300]], axis=0)
hrs1 = hrs1.reset_index(drop=True)
hrs2 = pd.concat([hrswork[300:599], hrsstill[300:600]], axis=0)
hrs2 = hrs2.reset_index(drop=True)
hrs3 = pd.concat([hrswork[599:860], hrsstill[600:899]], axis=0)
hrs3 = hrs3.reset_index(drop=True)

## label
# [76,82,84,82,86,86,90,88,90,90,88] [83,82,84,85,83,87,86,88,86,84,82]    85,85,81,82,82,83,85,82.5,83,87.5
gnd1 = [82,84,82,86,86,87,86,88,86,84] #29-33  #45-49
gnd2 = [85,85,81,82,82,90,88,90,90,88] #34-38  #8-12
gnd3 = [83,82,82.5,86,87.5,83,82,86,86,81] #40-44 #13-17

gnd=[82,84,82,86,86,90,88,90,90,88,83,82,86,86,81] #29-44
[87,86,88,86,84,85,85,81,82,82,83,82,82.5,86,87.5] #45-49 8-17

## Fitbit数据
path = './data/Fibit'
filelist = os.listdir(path)
path1 = os.path.join(path,filelist[4]) 
path2 = os.path.join(path,filelist[6])
path3 = os.path.join(path,filelist[5])
#extra data
hrfb = pd.read_excel(path1,names=['time','heart'])
hrfb = hrfb.sort_values('time')
hrfb = hrfb.reset_index(drop=True)
hrfb['heart'] = hrfb['heart'] + 9
# position1
hrfstill = pd.read_excel(path3,names=['time','heart'])
hrfstill = hrfstill.sort_values('time')
hrfstill = hrfstill.reset_index(drop=True)
# position2
hrfwork = pd.read_excel(path2,names=['time','heart'])
hrfwork = hrfwork.sort_values('time')
hrfwork = hrfwork.reset_index(drop=True)
# divided into three groups
hrf1 = pd.concat([hrfwork[8:48], hrfstill[39:78]], axis=0)
hrf1 = hrf1.reset_index(drop=True)
hrf2 = pd.concat([hrfwork[48:85], hrfb[0:38]], axis=0)
hrf2 = hrf2.reset_index(drop=True)
hrf3 = pd.concat([hrfstill[0:39], hrfb[38:76]], axis=0)
hrf3 = hrf3.reset_index(drop=True)

# merge
info1 = combine(hrs1, hrf1)
info2 = combine(hrs2, hrf2)
info3 = combine(hrs3, hrf3)
info = pd.concat([info1, info2, info3])


'''prepare the data(man data) for distribution picture'''
## all data(each second)
hrswork = padding(hrswork, count=39)
hrsstill = padding(hrsstill, count=0)
woman_hrs = pd.concat([hrswork,hrsstill])
woman_hrs = woman_hrs.reset_index(drop=True)
woman_hrs = woman_hrs.fillna(method='pad')

hrf_work = pd.concat([hrfwork[8:], hrfstill[0:39]])
hrf_work = hrf_work.reset_index(drop=True)
hrf_work = padding(hrf_work, count=24)

hrf_still = pd.concat([hrfstill[39:78], hrfb[0:76]])
hrf_still = hrf_still.reset_index(drop=True)
hrf_still = padding(hrf_still, count=8)

woman_hrf = pd.concat([hrf_work,hrf_still])
woman_hrf = woman_hrf.reset_index(drop=True)
woman_hrf = woman_hrf.fillna(method='pad')

# suplement the data to 30 minutes
woman_hrf = pd.concat([pd.DataFrame([79]*7,columns=['hr']), woman_hrf],axis=0)
woman_hrf = woman_hrf.reset_index(drop=True)

## mean data(each minute)
woman_info = info


## combine the all data of man and woman
hrf = pd.concat([man_hrf,woman_hrf], axis=0)
hrf = hrf.reset_index(drop=True)
hrs = pd.concat([man_hrs,woman_hrs], axis=0)
hrs = hrs.reset_index(drop=True)

gnd = [63,61,64,64,65,66,64,67,66,67,65,69,66,64,69,63,61,62,61,61,62,64,64,63,
       65,61,62,70,63,65,82,84,82,86,86,90,88,90,90,88,83,82,86,86,81,87,86,88,
       86,84,85,85,81,82,82,83,82,82.5,86,87.5]
# supplement the gnd data
hrg = pd.DataFrame()
for hrg_i in gnd:
    tmp = pd.DataFrame([hrg_i]*60)
    hrg = pd.concat([hrg, tmp], axis=0)
hrg = hrg.reset_index(drop=True)

## plot
hr = pd.concat([hrs, hrf, hrg], axis=1)
hr.columns = ['hrs', 'hrf', 'hrg']
pltt.plot_distribution(hr)



# plot mean distribution
## combine mean data of man and woman
mean_hr = pd.concat([man_info, woman_info], axis=0)
mean_hr = mean_hr.reset_index(drop=True)
mean_hr = pd.concat([mean_hr, pd.DataFrame(gnd)], axis=1)
mean_hr = mean_hr.drop(['time'], axis=1)
mean_hr.columns = ['hrs', 'hrf', 'hrg']

gnd = [63,61,64,64,65,63,61,62,61,61,66,64,67,66,67,62,64,64,63,65,65,69,66,64,
       69,61,62,70,63,65,82,84,82,86,86,87,86,88,86,84,85,85,81,82,82,90,88,90,
       90,88,83,82,82.5,86,87.5,83,82,86,86,81]

#plot
pltt.plot_distribution(hr)


##女生的标签
#gnd1 = [63,61,64,64,65,63,61,62,61,61]
#gnd1 = [66,64,67,66,67,62,64,64,63,65]
#gnd1 = [65,69,66,64,69,61,62,70,63,65]
#gnd1 = [63,61,64,64,65,63,61,62,61,61,66,64,67,66,67,62,64,64,63,65,65,69,66,64,69,61,62,70,63,65]
#
#
#gnd1 = [82,84,82,86,86,87,86,88,86,84] #29-33  #45-49
#gnd1 = [85,85,81,82,82,90,88,90,90,88] #34-38  #8-12
#gnd1 = [83,82,82.5,86,87.5,83,82,86,86,81] #40-44 #13-17
#gnd1 = [82,84,82,86,86,87,86,88,86,84,85,85,81,82,82,90,88,90,90,88,83,82,82.5,86,87.5,83,82,86,86,81]
#
##gnd1=[63.,61.,64.,64.,65.,66.,64.,67.,66.,67]
#gnd = [63,61,64,64,65,63,61,62,61,61,66,64,67,66,67,62,64,64,63,65,65,69,66,64,69,61,62,70,63,65,82,84,82,86,86,87,86,88,86,84,85,85,81,82,82,90,88,90,90,88,83,82,82.5,86,87.5,83,82,86,86,81]







    
    
    