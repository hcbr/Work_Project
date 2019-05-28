# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#显示数字
class plotpicture(object):

    def shownumber(self, rects):
        """show the text of bar picture"""
        for rect in rects:
            height = rect.get_height()
            plt.text(rect.get_x()+rect.get_width()/2 - 0.1 , 0.1+height, 
                     '%s' % float(height))

    def bar(self,y1, y2, xlabel='', ylabel='', xlim=[], ylim=[], title='', 
            save=False):
        """plot the bar"""
        x = list(range(len(y1))) 
        total_width = 0.8
        n = 2
        one_width = total_width / n
        a = plt.bar(x, y1, width = one_width, label='SensOmics', fc = 'b')
        for i in range(len(x)):
            x[i] = x[i] + one_width
        b = plt.bar(x, y2, width = one_width, label = 'Fitbit', fc = 'g')
        
        self.shownumber(a)
        self.shownumber(b)
        for i in range(len(x)): #adjust the coordinate
            x[i] = x[i] -0.2
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend()
        #plt.xlim(xlim)
        plt.ylim(ylim)
        plt.xticks(x,['1','2','3']) #change the corrdinate to text
        if save == True:
            pic_name = input("input the picture name:")
            plt.savefig('./picture/'+pic_name+'.jpg', dpi=600)
            plt.savefig('./picture/'+pic_name+'.eps', dpi=600)
        plt.show()
        plt.close()
    
    def mean_fitting(self, y1, y2, gnd, ylim=[50,90]):
        """plot the mean value fitting picture"""
        x = list(range(len(y1)))
        def fitting(x, y):
            z = np.polyfit(x, y, 15)
            p1 = np.poly1d(z)
            y_new = p1(x)
            return y_new
        y1_new = fitting(x, y1)
        y2_new = fitting(x, y2)
        gnd_new = fitting(x, gnd)
        plt.plot(x,y1_new,color='b', label = 'SensOmics')
        plt.plot(x,y2_new,color='g', label = 'Fitbit')
        plt.plot(x,gnd_new,color='r', label = 'Omron')
        plt.title('Mean Regression')
        plt.ylim(ylim)
        plt.xlabel('time (min)')
        plt.legend()
        plt.show()
        plt.close()
               
    def plot_sequentially(self,hrs, hrf ,hrg, save=False):
        """plot the sequentially picture"""
        #hr = pd.concat([hrs[0:959], hrf[0:959], hrg[0:959]], axis=1)
        hr = pd.concat([hrs['hr'][0:580], hrf[0:580], hrg[0:580]], axis=1)
        hr.columns = ['hrs', 'hrf', 'hrg']
        plt.figure() 
        plt.plot(hr['hrs'], 'b*')
        plt.plot(hr['hrf'].dropna(), 'g^')
        plt.plot(hr['hrg'].dropna(), 'rs')
        plt.xlabel('Seconds', fontsize=15)
        #plt.yticks(fontsize=12)
        plt.ylabel('Heartrate/bpm', fontsize=15)
        plt.legend(labels = ['Sens', 'Fitbit', 'GND'], loc = 'best')
        if save == True:
            plt.savefig('./picture/woman-time3-2.jpg', dpi=600)
            plt.savefig('./picture/woman-time3-2.eps', dpi=600)
       
    def plot_distribution(self, hr):
        """plot the distribution picture"""
        hr_ = hr.copy()
        hr_['hrs'] = hr_['hrs'] - hr_['hrg']
        hr_['hrf'] = hr_['hrf'] - hr_['hrg']
        
        import seaborn as sns
        sns.set_style('darkgrid')
        sns.set_context('paper')
        #不发出警告
        import warnings
        warnings.filterwarnings('ignore')
        plt.figure()
        sns.distplot(pd.Series(hr_['hrs']), hist = True, 
                    kde = True, norm_hist = True,
                    rug = True, vertical = False,
                    color = 'g', label = 'Sens', axlabel = 'Residual')
        sns.distplot(pd.Series(hr_['hrf']), hist = True, 
                    kde = True, norm_hist = True,
                    rug = True, vertical = False,
                    color = 'b', label = 'Fitbit', axlabel = 'Residual')
        plt.legend()
   
        f, ax= plt.subplots()
        sns.kdeplot(hr_['hrs'], shade=True, color='g', label='Sens')
        sns.kdeplot(hr_['hrf'], shade=True, color='b', label='Fitbit')
        ax.set_title('Density Distribution')
        ax.set_xlabel('Residual', fontsize=10)
        ax.set_ylabel('Density',  fontsize=10)
        plt.vlines(0, 0, 1, colors='g', linestyles=':')
        plt.vlines(-1, 0, 1, colors='b', linestyles=':')
        plt.annotate(r'$\mu$ = 0', xy=(0, 0.13), 
                     xycoords='data', xytext=(+40, -20),
                     textcoords='offset points', fontsize=12, va='bottom', ha='left',
                     arrowprops=dict(arrowstyle='->', connectionstyle="arc3,rad=.5"))
        plt.annotate(r'$\mu$ = -1', xy=(-1, 0.08), 
                     xycoords='data', xytext=(-50, -20),
                     textcoords='offset points', fontsize=12, va='bottom', ha='left',
                     arrowprops=dict(arrowstyle='->', connectionstyle="arc3,rad=.5"))
      
        
        import seaborn as sns
        sns.set_style('darkgrid')
        sns.set_context('paper')
        #不发出警告
        import warnings
        warnings.filterwarnings('ignore')
        plt.figure()
        sns.distplot(pd.Series(hr_['hrs']), hist = True, 
                    kde = True, norm_hist = True,
                    rug = True, vertical = False,
                    color = 'g', label = 'Sens', axlabel = 'Residual')
        sns.distplot(pd.Series(hr_['hrf']+2), hist = True, 
                    kde = True, norm_hist = True,
                    rug = True, vertical = False,
                    color = 'b', label = 'Fitbit', axlabel = 'Residual')
        plt.legend()
        
        f, ax= plt.subplots()
        sns.kdeplot(hr_['hrs'], shade=True, color='g', label='Sens')
        sns.kdeplot(hr_['hrf'], shade=True, color='b', label='Fitbit')
        ax.set_title('Density Distribution')
        ax.set_xlabel('Residual', fontsize=10)
        ax.set_ylabel('Density',  fontsize=10)
        plt.vlines(0, 0, 1, linestyles=':')
        plt.annotate(r'$\sigma$ = 1.352', xy=(1.5, 0.13), 
                     xycoords='data', xytext=(+50, +10),
                     textcoords='offset points', fontsize=12, va='bottom', ha='left',
                     arrowprops=dict(arrowstyle='->', connectionstyle="arc3,rad=.5"))
        plt.annotate(r'$\sigma$ = 1.602', xy=(3.4, 0.08), 
                     xycoords='data', xytext=(+30, +10),
                     textcoords='offset points', fontsize=12, va='bottom', ha='left',
                     arrowprops=dict(arrowstyle='->', connectionstyle="arc3,rad=.5"))
        plt.show()
        plt.close()
        
        
        
        
        
        
        
        
        
        
        
        
##用pandas画
#y1 = [0.9110, 4.11]
#y2 = [0.7384, 9.06]
#woman1 = pd.DataFrame({'SensOmics':y1,'Fitbit':y2},index=['Correlation coefficient','Mse'])
#woman1.plot.bar(ylim=[0,10],rot=0, color=['g','b'])




#调用  
#man-still
#y1 = [0.676,2.32,1.63]
#y2 = [1.24,2.89,5.09]
#pltt = plotpicture()
#pltt.bar(y1, y2, xlabel='Experiment sets',ylabel='Mse',ylim=[0,7],title="Regression correlation",save=False)
#bar(y1, y2, xlabel='Experiment sets',ylabel='Correlation coefficient',title="Spearman's rank correlation coefficient")

#y1 = [0.8562,1.2884,1.3264,1.2842,1.3069]
#y2 = [1.4734,2.0716,2.0779,2.0779,2.2566]

#manworking
#y1 = [0.820,0.795,0.858,0.877,0.841]
#y2 = [0.722,0.758,0.812,0.893,0.751]

#y1 = [2.002,2.007,2.048,1.877,2.348]
#y2 = [2.878,2.855,4.24,4.23,5.356]
#
##bar(y1,y2, label = 'Correlation value')
#bar(y1,y2, label = 'MSE value')



#男still
#y1 = [63.56,62.11,64.78,64.,64.14,66.4,64.57,65.,65.78,66.,66.,66.75,67.29,64.38,69.5]
#y2 = [61.44,60.89,63.56,63.25,64.29,65.,64.29,65.,65.,64.75,66.17,66.,66.29,64.88,67.6]
#gnd = [63.,61.,64.,64.,65.,66.,64.,67.,66.,67.,65.,69.,66.,64.,69.]

#男working
#info1 = pd.merge(hrs1,hrf1, on='time')
#info1['time'] = info1['time'].apply(lambda x: tans2min(x))
#info1 = info1.groupby(['time']).mean()
#info1 = info1.reset_index()
#
#info2 = pd.merge(hrs2,hrf2, on='time')
#info2['time'] = info2['time'].apply(lambda x: tans2min(x))
#info2 = info2.groupby(['time']).mean()
#info2 = info2.reset_index()
#
#info3 = pd.merge(hrs3,hrf3, on='time')
#info3['time'] = info3['time'].apply(lambda x: tans2min(x))
#info3 = info3.groupby(['time']).mean()
#info3 = info3.reset_index()
#
#info = pd.concat([info1, info2, info3])




#y1 = info['hr']
#y2 = info['heart']
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
#
#cha1 = abs(np.array(y1) - np.array(gnd))
#
#cha2 = abs(np.array(y2) - np.array(gnd))
#
##bar(cha1,cha2,'Deviation value')
#
#

##plt.plot(x,y1,color='r',label = 'SensOmics')
##plt.scatter(x,y2,color='b',label = 'Fitbit')
##plt.scatter(x,gnd,color='y',label = 'Omron')
#
#


















