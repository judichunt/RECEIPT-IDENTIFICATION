# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 22:10:04 2017

@author: user
"""
import pandas as pd
import re
import difflib
import datetime
now = datetime.datetime.now()

regex = r"\d{2}(\/)\d{2}(\/)(20)?1[3-7]"

input_folder = 'C:/Users/user/Downloads/Aeon Predict/'
d_test_text = pd.read_csv(input_folder + 'ocr_testN.csv',encoding = "ISO-8859-1")
d_score = pd.read_csv(input_folder + 'scores.csv',encoding = "ISO-8859-1")

d_test_text['Date']=""
d_test_text['Subtotal']=""
d_test_text['TAX']=""

length=len(d_test_text['text'])
for i in range(length):
    print(i)
    matches = re.finditer(regex, str(d_test_text['text'][i]))
    for match in matches:
        d_test_text['Date'][i]="{match}".format(match = match.group())
        print ("{match}".format(match = match.group()))
        break
    lines=str(d_test_text['text'][i]).split('\n')
    for line in lines:
        a=line.split()
        if len(a)>1&len(difflib.get_close_matches('SUBTOTAL',a , 1, 0.6))==1:
            d_test_text['Subtotal'][i]=a[len(a)-1]
            #print (a[len(a)-1])
            break
    
    for line in lines:
        a=line.split()
        if len(a)>1&len(difflib.get_close_matches('TAX',a , 1, 0.6))==1:
            d_test_text['TAX'][i]=a[len(a)-1]
            #print (a[len(a)-1])
            break


full={"EXT_ID":d_score["EXT_ID"],"PredictionScore":d_score["PredictionScore"],"WalmartReceipt":d_score["WalmartReceipt"]}
d_full=pd.DataFrame(data=full)
d_full['Date']=d_test_text['Date']
d_full['Subtotal']=d_test_text['Subtotal']
d_full['TAX']=d_test_text['TAX']


d_full.to_csv('full_submission'+str(now.strftime("%Y-%m-%d-%H-%M"))+'.csv',index=False)  
