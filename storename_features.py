# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 23:15:23 2017

@author: user
"""

from PIL import Image, ImageEnhance, ImageFilter
from pytesseract import *
import numpy as np
import pandas as pd
import xgboost as xgb
from scipy import sparse
import matplotlib.pyplot as plt
from pylab import plot, show, subplot, specgram, imshow, savefig
import datetime
now = datetime.datetime.now()
import difflib
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.gaussian_process.kernels import WhiteKernel, Matern, RBF, DotProduct, RationalQuadratic
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split

#original_open = open
#def bin_open(filename, mode='rb'):       # note, the default mode now opens in binary
#    return original_open(filename, mode)


input_folder = 'C:/Users/user/Downloads/Aeon Predict/'
d_train_text = pd.read_csv(input_folder + 'ocr_train.csv',encoding = "ISO-8859-1")
d_test_text = pd.read_csv(input_folder + 'ocr_test.csv',encoding = "ISO-8859-1")
#d_test_text = pd.read_json(input_folder + 'ocr_test_1.json')
storename= ['TARGET','Walmart','TRADER JOES','WALGREEN']
keywords=['EXPECT MORE PAY LESS','Save money. Live better.']
for word in keywords:
    storename.append(word)

length=len(d_train_text['text'])
#length=30

for keyword in storename:
    d_train_text[keyword]=0 
    d_test_text[keyword]=0 


d_train_text['text_length']=0
for i in range(length):
    print(i)
    cleaned_text1=str(d_train_text['text'][i]).split('\n')
    cleaned_text2=str(d_train_text['text'][i]).split()
    d_train_text['text_length'][i]=len(cleaned_text2)
    for keyword in storename:
        if len(difflib.get_close_matches(keyword,cleaned_text1 , 1, 0.6)):                
            d_train_text[keyword][i]=1
            #print(i)
        elif len(difflib.get_close_matches(keyword,cleaned_text2 , 1, 0.6)):                
            d_train_text[keyword][i]=1
            #print(i)                        




d_train_text.to_csv('ocr_trainN'+str(now.strftime("%Y-%m-%d-%H-%M"))+'.csv',index=False)                        



y=d_train_text["IsWalmart"].values

d={'text_length':d_train_text['text_length']}
X=pd.DataFrame(data=d)
for keyword in storename:
    X[keyword]=d_train_text[keyword]
X['TA']=X["TARGET"]|X["EXPECT MORE PAY LESS"]
X['Wal']=X["Walmart"]|X["Save money. Live better."]






params = {}
params['objective'] = 'multi:softprob'
params['eval_metric'] = 'mlogloss'
params['num_class'] = 2
params['eta'] = 0.08
params['max_depth'] = 6
params['subsample'] = 0.7
params['colsample_bytree'] = 0.7
params['silent'] = 1
params['num_rounds'] = 350
params['seed'] = length

#xgb_train=xgb.DMatrix(np.array(X.values),label=np.array(y))
#clr=xgb.train(params, xgb_train, params['num_rounds'])



length=len(d_test_text['text'])


d_test_text['text_length']=0
for i in range(length):
    cleaned_text1=str(d_test_text['text'][i]).split('\n')
    cleaned_text2=str(d_test_text['text'][i]).split()
    d_test_text['text_length'][i]=len(cleaned_text2)
    for keyword in storename:
        if len(difflib.get_close_matches(keyword,cleaned_text1 , 1, 0.6)):                
            d_test_text[keyword][i]=1
            print(i)
        elif len(difflib.get_close_matches(keyword,cleaned_text2 , 1, 0.6)):                
            d_test_text[keyword][i]=1
            #print(i)                        


d={'text_length':d_test_text['text_length']}
X_test=pd.DataFrame(data=d)
for keyword in storename:
    X_test[keyword]=d_test_text[keyword]
X_test['TA']=X_test["TARGET"]|X_test["EXPECT MORE PAY LESS"]
X_test['Wal']=X_test["Walmart"]|X_test["Save money. Live better."]



x_train, x_vali, Y_train, Y_vali = train_test_split(X, y, test_size=0.25, random_state=42)

x_train_array = pd.DataFrame.as_matrix(x_train)
x_vali_array = pd.DataFrame.as_matrix(x_vali)
Y_train_array = Y_train
Y_vali_array = Y_vali
dtrain = xgb.DMatrix(x_train_array, label=Y_train_array)
dvali = xgb.DMatrix(x_vali_array, label=Y_vali_array)
x_array = pd.DataFrame.as_matrix(X)
dt = xgb.DMatrix(x_array, label=y)
dtest_array = xgb.DMatrix(pd.DataFrame.as_matrix(X_test))

param = {'max_depth':3, 'eta':1, 'silent':0, 'eval_metric':'rmse'}
evallist  = [(dvali,'eval'), (dtrain,'train')]
num_round = 30
bst = xgb.train(params,dt,num_round,evallist)

ypred = bst.predict(dtest_array)



cols={'EXT_ID':d_test_text['EXT_ID'],'PredictionScore':ypred[:,1],'WalmartReceipt':'FALSE'}
sub=pd.DataFrame(data=cols)

for i in range(length):
    if ypred[i][1]>0.5:
        sub['WalmartReceipt'][i]='TRUE'


d_test_text.to_csv('ocr_testN'+str(now.strftime("%Y-%m-%d-%H-%M"))+'.csv',index=False)  
sub.to_csv('scores'+str(now.strftime("%Y-%m-%d-%H-%M"))+'.csv',index=False) 


