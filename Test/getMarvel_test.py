
# coding: utf-8

# In[130]:

import numpy as np
import json

import requests
import hashlib
import time
import re

from sys import argv
from copy import deepcopy
import sys


# In[25]:
if len(argv)!=2:
    print "Wrong number of arguments"

filename=str(argv[1])
try:
    scrapingresult2012=filename
    with open(scrapingresult2012, 'r') as file:
           salestext=file.read()
    salesdata=json.loads(salestext)
    print "size of sales data: %s" %len(salesdata)
except:
    scrapingresult="sales.json"
    with open(scrapingresult, 'r') as file:
           sales=file.read()
    salesdata=json.loads(sales)





# In[13]:

monthtable={"January":"01", "February":"02", "March":"03", "April":"04", "May":"05", "June":"06", "July":"07", "August":"08", "September":"09", "October":"10", "November":"11", "December":"12"}
def modify(comic):
    newprice=re.sub(u"\$", "", comic['price'][0])
    neworder=re.sub(u",", "", comic['orders'][0])

    newtitle=" ".join(re.findall(r"\S+", comic['title'][0]))
    comic['price']=newprice
    comic['orders']=neworder

    comic['comictitle']=newtitle
    if comic['date']:
        dateparts=re.findall(r"\S+", comic['date'][0])
        month=dateparts[0]
        year=dateparts[1]

        try:
            monthnum=monthtable[month]
            if monthnum in ["01", "03", "05", "07", "08", "10", "12"]:
                monthend="31"
            elif monthnum in ["06", "04", "09", "11"]:
                monthend="30"
            else:
                monthend="28"

            comic["dateRange"]=year+"-"+monthnum+"-01%2C%20"+year+"-"+monthnum+"-"+monthend

        except KeyError:
            print "Month cannot be inserted"



    if isinstance(comic['issue'], unicode):
        issuenumberparts=re.findall(r"\S+", comic['issue'])
        positive=re.sub('^-', "", issuenumberparts[0])
        comic['issueNumber']=positive

    else:
        if comic['issue']and re.match('\S+', comic['issue'][0]):
            issuenumberparts=re.findall(r"\S+", comic['issue'][0])
            positive=re.sub('^-', "", issuenumberparts[0])
            comic['issueNumber']=positive

    return comic


#

#salesdataclean=map(lambda comic: modify(comic), salesdata)
salesdataclean=[]
for i in range(len(salesdata)):
    try:
        salesdataclean.append(modify(salesdata[i]))
    except:
        print i

print "Use comic books that rank 70 in monthly sales"
highranked=filter(lambda comic: int(comic["rank"][0])<70, salesdataclean)

print "Number of high-ranked publication used for API requests: %s" %len(highranked)



apikey1=["661b9e5c78c3f490fc3e09cf7d0031e1" ,"880ce7b198f95999f3223d8728fc9734db814952"]

keyset=[apikey1]




class MarvelAPIObject(object):
    BASE_URL = "http://gateway.marvel.com:80/v1/public"
    def __init__(self, apikey=None, privkey=None):
        self.API_KEY = apikey
        self.PRIV_KEY = privkey

    def inputdata(self, salesdata):
        self.salesdata=salesdata

    def inputjson(self, api_result):
        self.api_result=api_result

    def getHash(self, ts, priv_key, pub_key):
        return hashlib.md5(ts+priv_key+pub_key).hexdigest()

    def getComic(self):
        request_url = self.BASE_URL +"/comics"
        request_url += '?apikey=%s' % self.API_KEY
        #request_url += "&titleStartsWith=%s" %("%20".join(self.salesdata['comictitle'].split()))
        titleparts=re.findall(r"\S+", self.salesdata['comictitle'])
        request_url += "&titleStartsWith=%s" %titleparts[0]
        if 'issueNumber' in self.salesdata:
            request_url += "&issueNumber=%s" %(self.salesdata['issueNumber'])
        if 'dateRange' in self.salesdata:
            request_url += "&dateRange=%s" %(self.salesdata['dateRange'])

        ts = str(time.time())
        request_url += '&ts=%s' % ts
        request_url += '&hash=%s' % self.getHash(ts, self.PRIV_KEY, self.API_KEY)
        self.requesturl=request_url
        return requests.get(request_url)




def api_collect(records):
    responses=[]
    counter=0
    N=len(records)

    keycounter=0
    #responsecounter=0
    for data in records:

        try:
            marvel=MarvelAPIObject(apikey=keyset[0][0], privkey=keyset[0][1])
            marvel.inputdata(data)
            apiresponse=marvel.getComic()
            result=json.loads(apiresponse.text)
            #print "%s results" %(responsecounter+1)
            #responsecounter+=1

            if result['code']==200:
                data['apiresult']=result
                responses.append(apiresponse)

            elif result['code']=="InvalidCredentials":
                print "Invalid key, check the key in code"
                break

            elif result['code']==429 or result['code']=="RequestThrottled" :
                if keycounter<3:

                    print "Limit reached for the day, stopped at request %s" %counter
                    break

            else:
                print "request failed, at the entry %s" %counter
        except:
            print "Error at entry %s" %counter
            data[u'apiresult']=['None']
            responses.append("None")

        finally:
            counter+=1
            data['url']=marvel.requesturl

    return records, responses


def save_object(obj, filename):
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


# In[24]:

#### run only once
responserecords2012_1, responseobjects2012_1=api_collect(highranked)

print "number of results retrieved: %s" %len(responseobjects2012_1)
with open('responses_test.json', 'w') as outfile:
    json.dump(responserecords2012_1, outfile, indent=1)



#save_object(responseobjects2012_1, 'response2012.pkl')
#save_object(responesrecords2012_1, 'responserecords2012_1.pkl')


# In[41]:



# In[63]:

##### run only once !!!



# In[33]:




# In[666]:
