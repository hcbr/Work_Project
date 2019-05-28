# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import scipy.stats
from sklearn import metrics


class Correlation:
    
    
    def __init__(self,data,gnd):
        self.data = data
        self.gnd = gnd
    
    
    def getresult(self):  # Spearman correlation
        if len(self.data) != len(self.gnd):
            print("wrong:the shape of inputs data need same")
        else:
            correlation = scipy.stats.spearmanr(self.data, self.gnd)
            mse = metrics.mean_squared_error(self.data, self.gnd)
        return correlation, mse
   
    
    def pearson(self):  #person correlation
        if len(self.data) != len(self.gnd):
            print("wrong:the shape of inputs data need same")
        p = self.data
        q = self.gnd
        result = scipy.stats.pearsonr(p, q)
        return result