
# coding: utf-8

# In[156]:

import numpy as np
import json
import hashlib 
import pickle
import csv
import pandas as pd
import sys

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.svm import SVC
from sklearn.svm import SVR


# In[140]:

comicdata=pd.read_csv('marvelherosall.csv', header=None, names=['Character', 'Role', 'Orders', 'Bookid', 'Title'])

comicdata['indicator'] = pd.Series(np.repeat(1, comicdata.shape[0]), index=comicdata.index)
#comicdata.head()


# In[141]:


indexed=comicdata[['Title', 'Character', 'indicator']]

indexed.head(15)
def selfirst(x):
    return x.iloc[0]

pivoted=indexed.pivot_table(index="Title", columns="Character", values="indicator", aggfunc=selfirst).fillna(0)

#pivoted.drop()
#pivoted.iloc[:,0:10].head()

#pivoted.loc["1602 Witch Hunter Angela (2015) #1 (Isanove Variant)",]


# In[142]:

salesnumber=comicdata[['Title', 'Orders']]
salesnumber.index=comicdata.index
#salesnumber.head()
def selfirst(x):
    return x.iloc[0]
salespivot=salesnumber.pivot_table(index="Title", values="Orders", aggfunc=selfirst)

salesnumber[salesnumber['Title']=="Ultimate War (2003) #4"]
#salespivot.head(20)




# In[143]:

np.random.seed(2312)
randindex=np.random.permutation(pivoted.shape[0])
randomgrid=pivoted.iloc[randindex, ]
randsales=salespivot.iloc[randindex,]

#if np.array_equal(randomgrid.index, randsales.index):
   # print "Data are ok"




# In[144]:

train_data=randomgrid.iloc[0:4999,]
train_data=train_data.astype('int64')
train_outcome=randsales.iloc[0:4999,]
train_labels=train_outcome.values.view('float64')
train_labels[:,]=train_outcome
#train_labels=np.array(train_labels, ndmin=2).reshape(len(train_labels), 1)



test_data=randomgrid.iloc[5000::,]
test_data=test_data.astype('int64')
test_outcome=randsales.iloc[5000::,]
test_labels=test_outcome.values.view('float64')
test_labels[:]=test_outcome
#test_labels=np.array(test_labels, ndmin=2).reshape(len(test_labels), 1)


#train_data.to_csv("train_data.csv", sep=",", encoding="utf8")
#train_outcome.to_csv("train_outcome.csv", sep=",", encoding="utf8")

#test_data.to_csv("test_data.csv", sep=",", encoding="utf8")
#test_outcome.to_csv("test_outcome.csv", sep=",", encoding="utf8")
print train_data.shape
print train_labels.shape


# In[151]:

def save_object(obj, filename):
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)
        
def trainmodel(train_data, dev_data, train_label=train_labels, dev_label=test_labels, params={ "kernel":"rbf"}):
    rf=SVR().set_params(**params)
    rf.fit(train_data, train_label)
    rf_pred=rf.predict(dev_data)
    #r2=mean_squared_error(dev_label, rf_pred)
    r2 = rf.score(dev_data, dev_label)  
    
    return r2, rf


# In[152]:

r2_1, rf1=trainmodel(train_data, test_data)
print "R2 of Support Vector Machine (closer to 1 the better): %s" %r2_1


# In[153]:

def trainmodel(train_data, dev_data, train_label=train_labels, dev_label=test_labels, params={}):
    rf=LinearRegression().set_params(**params)
    rf.fit(train_data, train_label)
    rf_pred=rf.predict(dev_data)
    #r2=mean_squared_error(dev_label, rf_pred)
    r2 = rf.score(dev_data, dev_label)  
    
    return r2, rf

r2_2, rf2=trainmodel(train_data, test_data)
print "R2 of Linear regression (closer to 1 the better): %s" %r2_2 


# In[158]:

def trainmodel(train_data, dev_data, train_label=train_labels, dev_label=test_labels, params={}):
    rf=RandomForestClassifier().set_params(**params)
    rf.fit(train_data, train_label)
    rf_pred=rf.predict(dev_data)
    #r2=mean_squared_error(dev_label, rf_pred)
    r2 = rf.score(dev_data, dev_label)  
    return r2, rf

r2_2, rf2=trainmodel(train_data, test_data, params={"n_estimators":100})
print "R2 of Random Forest (closer to 1 the better): %s" %r2_2 


# In[ ]:



