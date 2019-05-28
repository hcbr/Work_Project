# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 16:46:06 2019

@author: lsx
"""

import time
import pandas as pd

#filepath = './data/micro'
##savepath = './result'
#filelist = os.listdir(filepath)
#
#
#HR = [] # Heart Rate No.1
#ST = [] # Skin Temperature NO.2
#GS = [] # Galvanic skin reaction No.3
#AL = [] # Ambient light NO.4
#Ac = [] # Accelerometer No.5
#Gy = [] # Gyro No.6
#PM = [] # 其实是步数 No.7
#c = [] # 中间变量，分割后的每一行数据
#temp_time = 0 #临时时间，为了做对比
#
#    
#def read_mic(filepath):
#    
#    fodata = open(file=filepath, mode='rt', encoding='utf-8')
#    for line in fodata:
#        aline = fodata.readline()
#        b = aline.split(';')
#        c = []
#        for i in b:
#            try:
#                m = float(i)
#                c.append(m)
#            except ValueError:
#                i = None
#                c.append(i)
#        try:
#            dt = c[0] / 1000
#            dt = time.localtime(dt)
#            c[0] = time.strftime('%Y-%m-%d %H:%M:%S', dt)
#        except:
#            # print('time convert error')
#            # print(c)
#            pass
#
#        try:
#            if c[1] == 1:
#                HR.append(c)
#            elif c[1] == 2:
#                ST.append(c)
#            elif c[1] == 3:
#                GS.append(c)
#            elif c[1] == 4:
#                AL.append(c)
#            elif c[1] == 5:
#                Ac.append(c)
#            elif c[1] == 6:
#                Gy.append(c)
#            elif c[1] == 7:
#                PM.append(c)
#            else:
#                tempid = c[1]
#        except IndexError as e:
#            # print('index error')
#            pass
#    print('%s, OK' %filename)
#    return HR
#
#for filename in filelist[0:1]:
#    print(filename)            
#    datapath = os.path.join(filepath, filename)
#    hr = read_mic(datapath)
#    if not len(hr) == 0:
#        dfHR = pd.DataFrame(hr)
#        dfHR = dfHR.drop_duplicates()
#        dfHR = dfHR.iloc[:, 0:3]  # 只取前三列
#        dfHR.columns = ['time', 'id', 'hr']
#        dfHR['name'] = filename
#        dfHR['time'] = pd.to_datetime(dfHR['time'])  # print(dfHR)
#    else:
#        print('HR of %s is empty'%filename)
        
        
def parser(filepath):
    
    #时间戳转换
    def parse_time(stamp):
        stamp = stamp/1000     #why /1000
        dtime = time.localtime(stamp)
        dtime = time.strftime('%Y-%m-%d %H:%M:%S', dtime)
        return dtime
    
    
    hr = list() # Heart Rate No.1
    st = list() # Skin Temperature NO.2
    gs = list() # Galvanic skin reaction No.3
    al = list() # Ambient light NO.4
    ac = list() # Accelerometer No.5
    gy = list() # Gyro No.6
    pm = list() # Step No.7
    uk = list() # Unknown
        
    fodata = open(file=filepath, mode='rt', encoding='utf-8')
    for line in fodata:
        steam = fodata.readline()
        frame = steam.split(';')
        parse = list()
        for i in frame:
            try:
                parse.append(float(i))
            except ValueError:
                parse.append(None)
        try:
            parse[0] = parse_time(parse[0])
        except:
            pass
        
        try:
            flag = parse[1]
        except:
            pass
        
        try:
            if flag == 1:
                hr.append(parse)
            elif flag == 2:
                st.append(parse)
            elif flag == 3:
                gs.append(parse)
            elif flag == 4:
                al.append(parse)
            elif flag == 5:
                ac.append(parse)
            elif flag == 6:
                gy.append(parse)
            elif flag == 7:
                pm.append(parse)
            else:
                uk.append(parse)
        except IndexError as e:
            pass
    
    print('%s, OK' %filepath)
    if not len(hr) == 0:
        hr = pd.DataFrame(hr)
        hr = hr.drop_duplicates()
        hr = hr.iloc[:, :3]  # 只取前三列
        hr.columns = ['time', 'id', 'hr']
        hr['name'] = filepath
        hr['time'] = pd.to_datetime(hr['time'])
        return hr
    if not len(st) == 0:
        st = pd.DataFrame(st)
        st = st.drop_duplicates()
        st = st.iloc[:, :3]  # 只取前三列
        st.columns = ['time', 'id', 'hr']
        st['name'] = filepath
        st['time'] = pd.to_datetime(st['time'])
        return st
    if not len(ac) == 0:
        ac = pd.DataFrame(ac)
        ac = ac.drop_duplicates()
        ac = ac.iloc[:, :5]
        ac.columns = ['time', 'id', 'ac1', 'ac2', 'ac3']
        ac['name'] = filepath
        ac['time'] = pd.to_datetime(ac['time'])
        return ac
    if not len(gy) == 0:
        gy = pd.DataFrame(gy)
        gy = gy.drop_duplicates()
        gy = gy.iloc[:, :5]
        gy.columns = ['time', 'id', 'gy1', 'gy2', 'gy3']
        gy['name'] = filepath
        gy['time'] = pd.to_datetime(gy['time'])
        return gy
            
            
            
        
        
        
        
    