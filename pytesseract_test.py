# -*- codinimport builtins
from PIL import Image, ImageEnhance, ImageFilter
from pytesseract import *
import numpy as np
import pandas as pd
import xgboost as xgb
from scipy import sparse
import matplotlib.pyplot as plt
from pylab import plot, show, subplot, specgram, imshow, savefig
import builtins
import datetime
now = datetime.datetime.now()

original_open = open
def bin_open(filename, mode='rb'):       # note, the default mode now opens in binary
    return original_open(filename, mode)

import pytesseract

input_folder = 'C:/Users/user/Downloads/Aeon Predict/'
d_train = pd.read_csv(input_folder + 'training_data.csv')
d_test = pd.read_csv(input_folder + 'test_data.csv')
d_train['text']='';
d_test['text']='';

for i in range(len(d_test['EXT_ID'])):  
    #if i%2!=0:
    image_file = input_folder +'images/'+d_test['EXT_ID'][i]+'.jpg'
    img = Image.open(image_file)
    if img.size[0]>img.size[1]:
        img=img.rotate(-90)
    #img.show()
    enhancer = ImageEnhance.Contrast(img)
    images = enhancer.enhance(1)
    images = images.convert('L')
    #images = images.convert('1')
#    for j in range(1):
#        images=images.filter(ImageFilter.SHARPEN)
    for j in range(1):
        images=images.filter(ImageFilter.MedianFilter)
    #images.show()#len(d_train['EXT_ID'])
    
    try:
        builtins.open = bin_open
        bts = pytesseract.image_to_string(images,lang='eng')
    finally:
        builtins.open = original_open
    
    #print(str(bts, 'cp1252', 'ignore'))
    d_test['text'][i]=str(bts, 'cp1252', 'ignore')
    print(i)
    
d_test.to_csv('ocr_test'+str(now.strftime("%Y-%m-%d-%H-%M"))+'.csv',index=False)    


