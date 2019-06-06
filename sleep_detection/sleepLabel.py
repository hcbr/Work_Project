# -*- coding: utf-8 -*-

import pandas as pd
#import date as dt
import os
import senswatch

import datetime as dt
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn import metrics
import numpy as np


path = './data/11-21'
dirlist = os.listdir(path)

hrs = pd.DataFrame()
raw = pd.DataFrame()
for file in dirlist:
    filepath = os.path.join(path, file)
    raw1, conv, drop = senswatch.parser(filepath)
    
    raw1 = pd.DataFrame(raw1)
    conv = pd.DataFrame(conv)
    drop = pd.DataFrame(drop)
    
    hrs = pd.concat([hrs, conv])
    raw = pd.concat([raw, raw1])
raw.columns=['acc1', 'acc2', 'acc3', 'ppg', 'time'] # bug吧， ppg得重设

#去除心率异常（0）值
hrs=hrs.reset_index(drop=True)
hrs = hrs.drop(hrs[hrs['hr']<50].index)
hrs=hrs.reset_index(drop=True)


#class addLabel(object):
#    
#    def __init__(self, dataInfo, labelInfo):
#        self.dataInfo = dataInfo
#        self.labelInfo = labelInfo
#        
#    def transTime(self):
#        
#        def dataType(self):
#            strTime = dt.datatime.fromtimestamp(self.dataInfo['time']/1000).strftime('%Y-%m-%d %H:%M:%S')  #type:string
#            return dt.datetime.strptime(strTime, "%Y-%m-%d %H:%M:%S")  # tpye:datetime
#    

def transTime(time):
    strTime = dt.datetime.fromtimestamp(time/1000).strftime('%Y-%m-%d %H:%M:%S') #type:string
    return dt.datetime.strptime(strTime, "%Y-%m-%d %H:%M:%S")  # tpye:datetime
# 保留年月日的时间
#def transtomin(t):
#    return dt.datetime(t.year, t.month, t.day, t.hour, t.minute)

#只保留时间，不保留日期
def transtotime(t):
    return dt.time(t.hour, t.minute, t.second)

hrs['time'] = hrs['time'].apply(lambda t:transTime(t))
hrs = hrs.reset_index(drop=True)

raw['time'] = raw['time'].apply(lambda t:transTime(t))
raw = raw.reset_index(drop=True)

# 时间到分钟
hrs['time'] = hrs['time'].apply(lambda t:transtotime(t))
raw['time'] = raw['time'].apply(lambda t:transtotime(t))



# 添加RR列
hrs['RR'] = 60000 / hrs['hr']
# 添加HRV列
hrs['HRV'] = hrs['RR'].diff()

# 标准化
hrs['hr'] = (hrs['hr'] - hrs['hr'].mean()) / hrs['hr'].std()
hrs['RR'] = (hrs['RR'] - hrs['RR'].mean()) / hrs['RR'].std()
hrs['HRV'] = (hrs['HRV'] - hrs['HRV'].mean()) / hrs['HRV'].std()

raw['acc1'] = (raw['acc1'] - raw['acc1'].mean()) / raw['acc1'].std()
raw['acc2'] = (raw['acc2'] - raw['acc2'].mean()) / raw['acc2'].std()
raw['acc3'] = (raw['acc3'] - raw['acc3'].mean()) / raw['acc3'].std()
raw['ppg'] = (raw['ppg'] - raw['ppg'].mean()) / raw['ppg'].std()

#去空
hrs = hrs.dropna()
raw = raw.dropna()

hrs = hrs.reset_index(drop=True)  
raw = raw.reset_index(drop=True) 

#均值
meanhrs = hrs.groupby(['time']).mean()
meanraw = raw.groupby(['time']).mean()
mean = pd.merge(meanhrs, meanraw, on='time')
mean.columns = ['mean_hr', 'meanRR', 'meanHRV', 'meanac1', 'meanac2', 'meanac3', 'meanppg']

#最大值
arghrs = hrs.groupby(['time']).max()
maxraw = raw.groupby(['time']).max()
maxAll = pd.merge(arghrs, maxraw, on='time')
maxAll.columns = ['max_hr', 'maxRR', 'maxHRV', 'maxac1', 'maxac2', 'maxac3', 'maxppg']
#最小值
minhrs = hrs.groupby(['time']).min()
minraw = raw.groupby(['time']).min()
minAll = pd.merge(minhrs, minraw, on='time')
minAll.columns = ['min_hr', 'minRR', 'minHRV', 'minac1', 'minac2', 'minac3', 'minppg']

#中位数
medianhrs = hrs.groupby(['time']).median()
medianraw = raw.groupby(['time']).median()
medianAll = pd.merge(medianhrs, medianraw, on='time')
medianAll.columns = ['medianhr', 'medianRR', 'medianHRV', 'medianac1', 'medianac2', 'medianac3', 'medianppg']

#std
stdhrs = hrs.groupby(['time']).std()
stdraw = raw.groupby(['time']).std()
stdAll = pd.merge(stdhrs, stdraw, on='time')
stdAll.columns = ['stdhr', 'stdRR', 'stdHRV', 'stdac1', 'stdac2', 'stdac3', 'stdppg']

data = pd.concat([mean, maxAll, minAll, medianAll, stdAll], axis=1)




#hrs['label'] = 0
#
#
#
#labelPath = './data/label.xls'
#labelinfo = pd.read_excel(labelPath)
#
#
#for i in range(len(labelinfo)):
#    start = hrs[hrs['time'] == labelinfo['start'][i]].index[0]
#    end = hrs[hrs['time'] == labelinfo['end'][i]].index[-1]
#    hrs['label'][start:end+1] = labelinfo['label'][i]
    
 


    
#dateStart = hrs['time'].iloc[0] 
#dateEnd = hrs['time'].iloc[-1]

## 有日期的时间进行划分（同一天） 

#def splitSleep(info):
#
#    if dateStart.date() == dateEnd.date():    #同一天
#        day = dateStart.date().strftime("%Y-%m-%d")
#        # sleep time
#        sleepStart = day + ' 00:00:00'
#        sleepStart = dt.datetime.strptime(sleepStart, "%Y-%m-%d %H:%M:%S")
#        sleepEnd = day + ' 06:00:00'
#        sleepEnd = dt.datetime.strptime(sleepEnd, "%Y-%m-%d %H:%M:%S")
#        # active time
#        activeStart = day + ' 10:00:00'
#        activeStart = dt.datetime.strptime(activeStart, "%Y-%m-%d %H:%M:%S")
#        activeEnd = day + ' 18:00:00'
#        activeEnd = dt.datetime.strptime(activeEnd, "%Y-%m-%d %H:%M:%S")
#        
#        Sleep = info[(sleepStart< info['time']) & (info['time']<sleepEnd)]
#        Active = info[(activeStart< info['time']) & (info['time']<activeEnd)]
#        return Sleep, Active


## 只根据time划分，不管日期

def splitSleep(data):

    # sleep time
    sleepStart = dt.time(0, 0)  #0点
    sleepEnd = dt.time(6, 0)  #6点
    # active time
    activeStart = dt.time(10, 0)
    activeEnd = dt.time(18, 0)
    
    Sleep = data[(sleepStart< data.index) & (data.index <sleepEnd)]
    Active = data[(activeStart< data.index) & (data.index <activeEnd)]
    return Sleep, Active    

      
# 划分睡觉和活动
Sleep, Active = splitSleep(data)   
#rawSleep, rawActive = splitSleep(raw)

Sleep['label'] = 1
Sleep = Sleep.fillna(value=0)
Active['label'] = 0
Active = Active.fillna(value=0)

dataInfo = pd.concat([Sleep, Active], axis=0)

dataInfo.to_csv('./data/11-21.csv')

# 分类






'''下面的注释是用的时间窗（要改善）'''

## 以时间为索引
#hrsSleep = hrsSleep.set_index('time')
#hrsActive = hrsActive.set_index('time')
#rawSleep = rawSleep.set_index('time')
#rawActive = rawActive.set_index('time')



# active

#winLen = 3    #时间窗长度
#active_feature = [] #存放每段时间求得的特征
#
#hrsActive.index[-1] - hrsActive.index[0]
#for i in range(5):
#    record = []     # 存放一个时间段的特征
#    winStart = dateStart + dt.timedelta(minutes = (winLen*i))
#    winend = dateStart + dt.timedelta(minutes = (winLen*(i+1)))
#    
#    hrSelect = hrsActive.loc[winStart:winend, ['hr', 'RR', 'HRV']]
#    rawSelect = rawActive.loc[winStart:winend, ['acc1', 'acc2', 'acc3', 'ppg']]
#    
#    # 获取特征
#    record.append(np.mean(hrSelect['hr']))
#    record.append(np.median(hrSelect['hr']))
#    record.append(np.std(hrSelect['hr']))
#    record.append(np.max(hrSelect['hr']))
#    record.append(np.min(hrSelect['hr']))
#    record.append(np.mean(hrSelect['RR']))
#    record.append(np.median(hrSelect['RR']))
#    record.append(np.std(hrSelect['RR']))
#    record.append(np.max(hrSelect['RR']))
#    record.append(np.min(hrSelect['RR']))
#    record.append(np.mean(hrSelect['HRV']))
#    record.append(np.median(hrSelect['HRV']))
#    record.append(np.std(hrSelect['HRV']))
#    record.append(np.max(hrSelect['HRV']))
#    record.append(np.min(hrSelect['HRV']))
#    #             NN50 = dfHRselect[dfHRselect['HRV'] > 50]['HRV'].count()
#    # record.append(NN50/len(dfHRselect))
#    #             record.append(NN50)
#    record.append(np.mean(rawSelect['acc1']))
#    record.append(np.median(rawSelect['acc1']))
#    record.append(np.std(rawSelect['acc1']))
#    record.append(np.max(rawSelect['acc1']))
#    record.append(np.min(rawSelect['acc1']))
#    record.append(np.mean(rawSelect['acc2']))
#    record.append(np.median(rawSelect['acc2']))
#    record.append(np.std(rawSelect['acc2']))
#    record.append(np.max(rawSelect['acc2']))
#    record.append(np.min(rawSelect['acc2']))
#    record.append(np.mean(rawSelect['acc3']))
#    record.append(np.median(rawSelect['acc3']))
#    record.append(np.std(rawSelect['acc3']))
#    record.append(np.max(rawSelect['acc3']))
#    record.append(np.min(rawSelect['acc3']))
#    
#    active_feature.append(record)
#    
#    
#active_feature = pd.DataFrame(active_feature)
#active_feature.columns = ['mean_hr', 'median_hr', 'std_hr', 'max_hr', 'min_hr',
#                 'mean_RR', 'median_RR', 'std_RR', 'max_RR', 'min_RR',
#                 'mean_HRV', 'median_HRV', 'std_HRV', 'max_HRV', 'min_HRV', 'mean_ac1', 'median_ac1',
#                 'std_ac1', 'max_ac1', 'min_ac1', 'mean_ac2', 'median_ac2', 'std_ac2',
#                 'max_ac2', 'min_ac2', 'mean_ac3', 'median_ac3', 'std_ac3', 'max_ac3', 'min_ac3']


    





