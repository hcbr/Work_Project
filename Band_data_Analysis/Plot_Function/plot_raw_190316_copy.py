# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 14:40:10 2019

@author: lsx
"""

import pandas as pd
import numpy as np
import os
import sensomicsbandV123 as sob
import matplotlib.pyplot as plt

cols = ['time', 'hr']
### Read data
f_datapath = './data/sens/3-14/3-14-fitbit/fitbit2019-3-14-1.xls'
f_data = pd.read_excel(f_datapath, header=None)
f_data.columns = cols
f_data = f_data[::-1]
f_data = f_data.reset_index(drop=True)
#inter = pd.DataFrame([None]*7)
#hrf = pd.DataFrame()
#for hrf_i in f_data['hr']:
#    tmp = pd.concat([pd.DataFrame([hrf_i]),inter], axis=0)
#    hrf = pd.concat([hrf, tmp], axis=0)
#hrf = hrf.reset_index(drop=True)

def miss_value(f_data):
    miss_all = []
    for i in range(len(f_data)-1):
        miss = int((f_data['time'][i+1] - f_data['time'][i]).seconds)
        miss_all.append((miss)-1)
    return miss_all
f_miss = miss_value(f_data)

def padding(f_data,f_miss):
    hrf = pd.DataFrame()
    hr =  f_data['hr']
    for i in range(len(hr)-1):
        pad_value = pd.DataFrame([None]*f_miss[i])
        tmp = pd.concat([pd.DataFrame([hr[i]]),pad_value],axis=0)
        hrf = pd.concat([hrf,tmp],axis=0)
    hrf = pd.concat([hrf,pd.DataFrame([hr[len(hr)-1]])])
    return hrf
hrf =  padding(f_data,f_miss)  
hrf.columns = ['hr'] 
hrf = hrf.reset_index(drop=True)       


filepath = './data/sens/3-14/3-14-sense'
filelist = os.listdir(filepath)
hrs = pd.DataFrame()
raw = pd.DataFrame()
for file in filelist[0:12]:
    print(file)
    path = os.path.join(filepath, file)
    tmp, temp, error = sob.parser(path, mertic='sec')
    hrs = pd.concat([hrs, temp])
    raw = pd.concat([raw, tmp])
hrs_ = hrs.reset_index(drop=True)
hrs = hrs_.drop(['time'], axis=1)

inter = pd.DataFrame([None]*59) 
gnd = [65,63,65,64,64,64,66,66,65,67,65,64,70,65,70,66]
hrg = pd.DataFrame()
for hrg_i in gnd:
    tmp = pd.concat([pd.DataFrame([hrg_i]),inter], axis=0)
    hrg = pd.concat([hrg, tmp], axis=0)
hrg = hrg.reset_index(drop=True)

record_time = ['16-00-00', '16-04-00', '16-08-00', '16-12-00']
record_loc = [0, 240, 480, 720]


plt.figure()
#hr = pd.concat([hrs[0:959], hrf[0:959], hrg[0:959]], axis=1)
hr = pd.concat([hrs[0:605], hrf[0:605], hrg[0:605]], axis=1)
hr.columns = ['hrs', 'hrf', 'hrg']
plt.figure() 
plt.plot(hr['hrs'], 'g')
plt.plot(hr['hrf'].dropna(), 'b*')
plt.plot(hr['hrg'].dropna(), 'rs')
plt.xlabel('Seconds', fontsize=15)
plt.yticks(fontsize=12)
plt.ylabel('Heartrate/bpm', fontsize=15)
plt.legend(labels = ['Sens', 'Fitbit', 'GND'], loc = 'upper left')

#plt.annotate(r'$2x+1=%s$' % y0, xy=(x0, y0), xycoords='data', xytext=(+30, -30),
#             textcoords='offset points', fontsize=10,
#             arrowprops=dict(arrowstyle='->', connectionstyle="arc3,rad=.2"))
plt.annotate('16-00-00', xy=(0, 65), 
             xycoords='data', xytext=(+10, +20),
             textcoords='offset points', fontsize=12, va='bottom', ha='left',
             arrowprops=dict(arrowstyle='->', connectionstyle="arc3,rad=.5"))

plt.annotate('16-04-00', xy=(240, 64),
             xycoords='data', xytext=(+10, -25),
             textcoords='offset points', fontsize=12, va='top', ha='left',
             arrowprops=dict(arrowstyle='->', connectionstyle="arc3,rad=-.1"))

plt.annotate('16-08-00', xy=(480, 65), 
             xycoords='data', xytext=(+10, -30),
             textcoords='offset points', fontsize=12, va='top', ha='left',
             arrowprops=dict(arrowstyle='->', connectionstyle="arc3,rad=-.1"))


plt.figure()
hr = pd.concat([hrs[600:959], hrf[600:959], hrg[600:959]], axis=1)
hr = hr.reset_index(drop=True)
hr.columns = ['hrs', 'hrf', 'hrg']
plt.figure() 
plt.plot(hr['hrs'], 'g')
plt.plot(hr['hrf'].dropna(), 'b*')
plt.plot(hr['hrg'].dropna(), 'rs')
plt.xlabel('Seconds', fontsize=15)
plt.yticks(fontsize=12)
plt.ylabel('Heartrate/bpm', fontsize=15)
plt.legend(labels = ['Sens', 'Fitbit', 'GND'], loc = 'upper left')

plt.annotate('16-12-00', xy=(120, 70), 
             xycoords='data', xytext=(-20, +30),
             textcoords='offset points', fontsize=12, va='top', ha='left',
             arrowprops=dict(arrowstyle='->', connectionstyle="arc3,rad=-.1"))

plt.annotate('16-14-00', xy=(240, 70), 
             xycoords='data', xytext=(-5, +30),
             textcoords='offset points', fontsize=12, va='top', ha='left',
             arrowprops=dict(arrowstyle='->', connectionstyle="arc3,rad=-.1"))






###
###
###
cols = ['time', 'hr']
### Read data
f_datapath = './data314/3-14-fitbit/fitbit2019-3-14-2.csv'
f_data = pd.read_csv(f_datapath, header=None)
f_data.columns = cols
f_data = f_data[::-1]
f_data = f_data.reset_index(drop=True)
inter = pd.DataFrame([None]*7)
hrf = pd.DataFrame()
for hrf_i in f_data['hr']:
    tmp = pd.concat([pd.DataFrame([hrf_i]),inter], axis=0)
    hrf = pd.concat([hrf, tmp], axis=0)
hrf = hrf.reset_index(drop=True)

filepath = './data314/3-14-sense'
filelist = os.listdir(filepath)
hrs = pd.DataFrame()
raw = pd.DataFrame()
for file in filelist[24:37]:
    print(file)
    path = os.path.join(filepath, file)
    tmp, temp, error = sob.parser(path, mertic='sec')
    hrs = pd.concat([hrs, temp])
    raw = pd.concat([raw, tmp])
hrs_ = hrs.reset_index(drop=True)
hrs = hrs_.drop(['time'], axis=1)

inter = pd.DataFrame([None]*59) 
gnd = [63,65,62,61,61,62,64,64,63,65,61,62,62,63,65,61]
hrg = pd.DataFrame()
for hrg_i in gnd:
    tmp = pd.concat([pd.DataFrame([hrg_i]),inter], axis=0)
    hrg = pd.concat([hrg, tmp], axis=0)
hrg = hrg.reset_index(drop=True)

record_time = ['16-00-00', '16-04-00', '16-08-00', '16-12-00']
record_loc = [0, 240, 480, 720]


plt.figure()
#hr = pd.concat([hrs[0:959], hrf[0:959], hrg[0:959]], axis=1)
hr = pd.concat([hrs[0:605], hrf[0:605], hrg[0:605]], axis=1)
hr.columns = ['hrs', 'hrf', 'hrg']
plt.figure() 
plt.plot(hr['hrs'], 'g')
plt.plot(hr['hrf'].dropna(), 'b*')
plt.plot(hr['hrg'].dropna(), 'rs')
plt.xlabel('Seconds', fontsize=15)
plt.yticks(fontsize=12)
plt.ylabel('Heartrate/bpm', fontsize=15)
plt.legend(labels = ['Sens', 'Fitbit', 'GND'], loc = 'upper left')

#plt.annotate(r'$2x+1=%s$' % y0, xy=(x0, y0), xycoords='data', xytext=(+30, -30),
#             textcoords='offset points', fontsize=10,
#             arrowprops=dict(arrowstyle='->', connectionstyle="arc3,rad=.2"))
plt.annotate('16-00-00', xy=(0, 63), 
             xycoords='data', xytext=(+10, +20),
             textcoords='offset points', fontsize=12, va='bottom', ha='left',
             arrowprops=dict(arrowstyle='->', connectionstyle="arc3,rad=.5"))

plt.annotate('16-04-00', xy=(240, 61),
             xycoords='data', xytext=(+10, -25),
             textcoords='offset points', fontsize=12, va='top', ha='left',
             arrowprops=dict(arrowstyle='->', connectionstyle="arc3,rad=-.1"))

plt.annotate('16-08-00', xy=(480, 63), 
             xycoords='data', xytext=(+10, -30),
             textcoords='offset points', fontsize=12, va='top', ha='left',
             arrowprops=dict(arrowstyle='->', connectionstyle="arc3,rad=-.1"))


plt.figure()
hr = pd.concat([hrs[600:959], hrf[600:959], hrg[600:959]], axis=1)
hr = hr.reset_index(drop=True)
hr.columns = ['hrs', 'hrf', 'hrg']
plt.figure() 
plt.plot(hr['hrs'], 'g')
plt.plot(hr['hrf'].dropna(), 'b*')
plt.plot(hr['hrg'].dropna(), 'rs')
plt.xlabel('Seconds', fontsize=15)
plt.yticks(fontsize=12)
plt.ylabel('Heartrate/bpm', fontsize=15)
plt.legend(labels = ['Sens', 'Fitbit', 'GND'], loc = 'upper left')

plt.annotate('16-12-00', xy=(120, 62), 
             xycoords='data', xytext=(-20, +30),
             textcoords='offset points', fontsize=12, va='top', ha='left',
             arrowprops=dict(arrowstyle='->', connectionstyle="arc3,rad=-.1"))

plt.annotate('16-14-00', xy=(240, 65), 
             xycoords='data', xytext=(-5, +30),
             textcoords='offset points', fontsize=12, va='top', ha='left',
             arrowprops=dict(arrowstyle='->', connectionstyle="arc3,rad=-.1"))

