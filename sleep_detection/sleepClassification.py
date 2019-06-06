import pandas as pd
import numpy as np
import xgboost 
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics

# 读数据
dataInfo = pd.read_csv('./data/11-21.csv')
dataInfo = dataInfo.drop(['time'], axis=1)

#转ndarrary
data = dataInfo.values

X = data[:, 0:35]
Y = data[:, -1]

# split train and test
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.25, random_state=123)
import collections
print(collections.Counter(y_test))  
# XGBoost

paras = {
    'n_estimators':400, #数的个数
    'learning_rate':0.1,#学习率
    'scale_pos_weight':1, #如果大于0，不平衡时有助于快速收敛
    'silent':0,#1则没有信息输出
    'subsample': 0.9, 
    'reg_lambda': 2, 
    'reg_alpha': 0, 
    'min_child_weight': 3, 
    'max_depth': 8, 
    'gamma': 0.1, 
    'colsample_bytree': 0.8,
    'eval_metric': 'auc'}

model = XGBClassifier(**paras)
model.fit(X_train, y_train)
ans = model.predict(X_test)

#correct = (y_test == ans).astype(float)
#accuracy = np.mean(correct)

# 准确率
accuracy = metrics.accuracy_score(y_test, ans)
# 召回率
recall = metrics.recall_score(y_test, ans)
# 精确率
precision = metrics.precision_score(y_test, ans)