
# coding: utf-8

# In[130]:

import numpy as np
import json
import regex
import requests
import hashlib 
import time
import re
import pickle
from sys import argv
from copy import deepcopy
import sys


# In[25]:

scrapingresult2012="sales2012.json"
with open(scrapingresult2012, 'r') as file:
       sales2012=file.read()
salesdata2012=json.loads(sales2012)

    
scrapingresult="sales.json"
with open(scrapingresult, 'r') as file:
       sales=file.read()
salesdata=json.loads(sales)

print len(salesdata)
salesdata.extend(salesdata2012)
print len(salesdata2012)
print len(salesdata)


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

toy=[{'price':['$2.3'], 'orders':['342,32'], 'issue':u'49', 'title':['ultimate war \n badass'], 'date':['November 2002']},
    {'price':['$2.3'], 'orders':['2312'], 'issue':['231'], 'title':['captain america \n something'], 'date':['January 2001']}]
#print toy[0]['issue'][0]=='\n'

newtoy = map(lambda x: modify(x), toy)
for data in newtoy: 
    if 'issueNumber' in data:
        print 'success'
    else: print 'fail'

print newtoy


# In[7]:




# In[14]:




# In[15]:

#print salesdata[5180]['issue'][0]
print salesdata[0]['price'][0]
re.sub("\$", "", salesdata[0]['price'][0])
print salesdata[0]['price'][0]


# In[32]:


#salesdataclean=map(lambda comic: modify(comic), salesdata)
salesdataclean=[]
for i in range(len(salesdata)):
    try: 
        salesdataclean.append(modify(salesdata[i]))
    except:
        print i

highranked=filter(lambda comic: int(comic["rank"][0])<100, salesdataclean)



print len(highranked)


# In[10]:




# In[11]:




# In[12]:




# In[13]:

#print "%20".join(salesdataclean[0]['title'][0].split())
#print "&dateRange=%s" %(salesdataclean[0]['dateRange'])
#def getHash(self, ts, priv_key, pub_key):   
    #return hashlib.md5(ts+priv_key+pub_key).hexdigest()
#url="http://gateway.marvel.com:80/v1/public/comics?dateRange=2011-03-01%2C%202011-04-01&titleStartsWith=fantastic%20four&apikey=661b9e5c78c3f490fc3e09cf7d0031e1"


# In[120]:

apikey1=["661b9e5c78c3f490fc3e09cf7d0031e1" , "880ce7b198f95999f3223d8728fc9734db814952"]
apikey2=["1e24b32d89dd4d1be2ef1a731be862e0", "db29858993590f4be5474d3309e02c06f920611e"]
apikey3=["636656992f16311c84a0dae9c57b6b37", "5a09833c71ac96af41f99195f22de8d43f4e79e7"]
apikey4=["f533202fd3710c1612840ea636103cb4", "035e2bbf1c6b64ae8dbde0134458487e0fe6321b"]
keyset=[apikey1, apikey2, apikey3, apikey4]


# In[121]:

#http://gateway.marvel.com:80/v1/public/comics?dateRange=2013-01-01%2C%202003-12-31&titleStartsWith=ultimate%20war&issueNumber=50&apikey=661b9e5c78c3f490fc3e09cf7d0031e1

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
        
print(highranked[0]['orders'])
#marvel=MarvelAPIObject()
#marvel.inputdata(part1[0])
#result2=marvel.getComic()

#marvel=MarvelAPIObject()
#marvel.inputdata(part1[20])
#result3=marvel.getComic()



# In[131]:




# Examples from getComic()
# http://gateway.marvel.com:80/v1/public/comics?apikey=661b9e5c78c3f490fc3e09cf7d0031e1&titleStartsWith=Ultimate%20War&issueNumber=4&dateRange=2003-01-01%2C%202003-12-31&ts=1461038456.58&hash=edc21f3e25200c5239cc51e3a61be3b9
# http://gateway.marvel.com:80/v1/public/comics?apikey=661b9e5c78c3f490fc3e09cf7d0031e1&titleStartsWith=Ultimates&issueNumber=11&dateRange=2003-01-01%2C%202003-12-31&ts=1461038456.74&hash=91f2a1abf6487859faadf500467824a7

# In[112]:

def api_collect(records):
    responses=[]
    counter=0
    N=len(records)

    keycounter=0
    #responsecounter=0
    for data in records:
        
        try:
            marvel=MarvelAPIObject()
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
                    
                    print "Limit reached for one key, switching to key %s" %(keycounter+1)
                    keycounter+=1
                    marvel.API_KEY=keyset[keycounter][0]
                    marvel.API_KEY=keyset[keycounter][1]
                    
                    apiresponse=marvel.getComic()
                    result=json.loads(apiresponse.text)
                    data['apiresult']=result
                    responses.append(apiresponse)
                    
                else: 
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





# In[113]:

trial1result, trialresponse=api_collect(highranked[10:15])


# In[61]:




# In[110]:

print trial1result[2]

with open('trialresponses.txt', 'w') as trialfile:
    json.dump(trial1result, trialfile)


# In[54]:

print len(highranked)
part1_2012=highranked[0:1699]
part2_2012=highranked[1700::]

print part1_2012[0]['orders']

print len(part2_2012)


# In[24]:

#### run only once
responserecords2012_1, responseobjects2012_1=api_collect(part1_2012)


# In[40]:


print len(responserecords2012_1)
with open('responses2012_1.txt', 'w') as outfile:
    json.dump(responserecords2012_1, outfile) 

def save_object(obj, filename):
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

#save_object(responseobjects2012_1, 'response2012.pkl')
#save_object(responesrecords2012_1, 'responserecords2012_1.pkl')


# In[41]:

print responserecords2012_1[0]['orders']


# In[63]:

##### run only once !!!
responserecords2012_2, responseobjects2012_2=api_collect(part2_2012)


# In[64]:

print responserecords2012_2[0]['orders']
    
print len(responserecords2012_2)
with open('responses2012_2.txt', 'w') as outfile:
    json.dump(responserecords2012_2, outfile) 

#save_object(responseobjects2012_2, 'response2012_2.pkl')
#save_object(responserecords2012_2, 'responserecords2012_2.pkl')


# -------------------------------------------**Records before 2012**-------------------------------------------

# In[ ]:

#### run only once !!
responserecords1, responseobjects1=api_collect(part1)


# In[ ]:

print len(responsepart1)
with open('part1responses.txt', 'w') as outfile:
    json.dump(responsepart1, outfile)

#save_object(responseobjects1, 'responseobjects1.pkl')


# In[ ]:

#### run only once !!
responserecords2, responseobjects2=api_collect(part2)


# In[ ]:

print len(responsepart2)
with open('part2responses.txt', 'w') as outfile:
    json.dump(responsepart2, outfile)

#save_object(responseobjects2, 'responseobjects2.pkl')    


# In[663]:

##### run only once !
responserecords3, responseobjects3=api_collect(part3)


# In[580]:

print len(responsepart3)
with open('part3responses.txt', 'w') as outfile:
    json.dump(responsepart3, outfile)
    
#save_object(responseobjects3, 'responseobjects3.pkl')    


# In[611]:


            


# In[655]:




# In[647]:

##### run only once !
responserecords4, responesobjects4=api_collect(part4)


# In[648]:

print len(responserecords4)
with open('part4responses.txt', 'w') as outfile:
    json.dump(responsepart4, outfile)
    


# In[651]:

##### run only once !
responserecords5, responesobjects5=api_collect(part5)


# In[653]:

print len(responserecords5)
with open('part5responses.txt', 'w') as outfile:
    json.dump(responserecords5, outfile)


# In[657]:




# In[33]:




# In[666]:




