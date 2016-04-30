
# coding: utf-8

# In[1]:

import numpy as np
import json
import regex
import requests
import time
import re


import sys, traceback
import csv
from itertools import groupby, combinations
from copy import deepcopy
import pandas as pd


# In[2]:

characterdata=pd.read_csv('CharList.txt', header=None, delimiter="\t", names=['Character', "Role", "Origin"])
characterdata.head()


# In[59]:

with open("part1responses.txt", 'r') as file1:
    lines1=file1.read()
data1=json.loads(lines1)

with open("part2responses.txt", 'r') as file2:
    lines2=file2.read()
data2=json.loads(lines2)

with open("part3responses.txt", 'r') as file3:
    lines3=file3.read()
data3=json.loads(lines3)

with open("part4responses.txt", 'r') as file4:
    lines4=file4.read()
data4=json.loads(lines4)

with open("part5responses.txt", 'r') as file5:
    lines5=file5.read()
data5=json.loads(lines5)

print len(data1), len(data2), len(data3), len(data4), len(data5)


# In[61]:

with open("responses2012_1.txt", 'r') as file6:
    lines6=file6.read()
data6=json.loads(lines6)

print len(data6)


with open("responses2012_2.txt", 'r') as file7:
    lines7=file7.read()
data7=json.loads(lines7)

print len(data7)


# In[104]:

marveltable=characterdata[characterdata['Origin']=='Marvel Comics']


newdata=pd.DataFrame([["Spider-man", "Heroic", "MarvelComics"],
        ["Ronan", "Villainous", "MarvelComics"],
        ["Iron Man", "Heroic", "MarvelComics"],
         ["Avengers", "Heroic", "MarvelComics"],
         ["X-men", "Heroic", "MarvelComics"],
         ["Fantastic Four", "Heroic", "MarvelComics"],
         ["Cabal", "Villainous", "MarvelComics"],
         ["Professor X", "Heroic", "MarvelComics"],
         ["Sinister Six", "Villainous", "MarvelComics"],
         ["Inhumans", "Heroic", "MarvelComics"],
         ["Excalibur", "Heroic", "MarvelComics"],
         ["X-Force", "Heroic", "MarvelComics"],
         ["Guardians of", "Heroic", "MarvelComics"],
         ["Ultron", "Villainous", "MarvelComics"],
         ["Spider-Man", "Heroic", "MarvelComics"],
         ["X-Men", "Heroic", "MarvelComics"]], columns=["Character", "Role", "Origin"])


"""chartable=np.append(chartable, np.array([["Ronan", "Villainous", "MarvelComics"]]), axis=0)
chartable=np.append(chartable, np.array([["Hope Summers", "Heroic", "MarvelComics"]]), axis=0)
chartable=np.append(chartable, np.array([["Iron Man", "Heroic", "MarvelComics"]]), axis=0)
chartable=np.append(chartable, np.array([["Avengers", "Heroic", "MarvelComics"]]), axis=0)
chartable=np.append(chartable, np.array([["X-men", "Heroic", "MarvelComics"]]), axis=0)
chartable=np.append(chartable, np.array([["Fantastic Four", "Heroic", "MarvelComics"]]), axis=0)
chartable=np.append(chartable, np.array([["Cabal", "Villainous", "MarvelComics"]]), axis=0)
chartable=np.append(chartable, np.array([["Professor X", "Heroic", "MarvelComics"]]), axis=0)
chartable=np.append(chartable, np.array([["Sinister Six", "Villainous", "MarvelComics"]]), axis=0)
chartable=np.append(chartable, np.array([["Inhumans", "Heroic", "MarvelComics"]]), axis=0)
chartable=np.append(chartable, np.array([["Excalibur", "Heroic", "MarvelComics"]]), axis=0)
chartable=np.append(chartable, np.array([["X-Force", "Heroic", "MarvelComics"]]), axis=0)
chartable=np.append(chartable, np.array([["Guardians of", "Heroic", "MarvelComics"]]), axis=0)
chartable=np.append(chartable, np.array([["Ultron", "Villainous", "MarvelComics"]]), axis=0)
chartable=np.append(chartable, np.array([["Spider-Man", "Heroic", "MarvelComics"]]), axis=0)
chartable=np.append(chartable, np.array([["X-Men", "Heroic", "MarvelComics"]]), axis=0)

charlist=np.transpose(chartable)
database=charlist[0]
charstring=" ".join(charlist[0])
chartable_list=chartable.tolist()
return database, chartable_list
databse, chartable_list=makedatabase(arrays)

print database[1:20]
print chartable_list[-10::]

print chartable[0:10]"""

newdata.head(10)
marveltable=marveltable.append(newdata, ignore_index=True)
marveltable[marveltable["Character"]=="Ronan"]
marveltable.tail()
database=marveltable['Character'].values
print type(database)


# In[105]:



def find_ngrams(input_list, n=2):
    wordtuples=zip(*[input_list[i:] for i in range(n)])
    bigram=[" ".join(s) for s in wordtuples]
    return bigram

#print ["War" in database]
description=data6[0]['apiresult']['data']['results'][0]['description']
print find_ngrams(description.split())


# In[114]:

print "Wolverine" in database
print np.where(database=="Wolverine")[0].tolist()[0]


# In[119]:

trial=data6[12]
if trial['apiresult']['data']['results']:
    print "Good to go"
else: 
    print "Nada"
    
apichar=trial['apiresult']['data']['results'][0]['characters']


print trial['apiresult']['data']['results'][0]['description']
trialparts=re.findall('\w+',trial['apiresult']['data']['results'][0]['description'] )

bookcharacter=[s for s in trialparts if s in database]

print "extracted character: %s" %bookcharacter
datachar=map(lambda item:item['name'], apichar['items'])
#print datachar
bookcharacter.extend(datachar)
print list(set(bookcharacter))
print type(database)
roles=marveltable["Role"].values
bookstatus=[roles[np.where(database=="Wolverine")[0].tolist()[0]] if s in database else "unknown" for s in [u'Wolverine', u'Hawkeye', u'Iron Man', u'Blash']]
print bookstatus
#print set([s for s in bookcharacter if s in database])




# In[42]:

#getbigram(["James Logan", 'Hawkeye (Ultimate)', 'blah blah blah', 'ironman'])
d=trial['apiresult']['data']['results'][0]['characters']['items'][0]['name']
order=trial['orders']
print order
#a=d.split(" ")
#b=getbigram(a)
#a.extend(b)
#tt=[s for s in a if s in database]



# In[126]:

def getbigram(input_list, n=2):
    wordtuples=zip(*[input_list[i:] for i in range(n)])
    bigram=[" ".join(s) for s in wordtuples]
    return bigram

def getChar(records, database, charinfo):
    counter=0
          
    for data in records:
        try:
            if isinstance(data['apiresult'], list):
                continue
                
            if 'data' not in data['apiresult']:
                continue     
                
            if not data['apiresult']['data']:
                continue 
                
            if 'results' not in data['apiresult']['data']:
                continue
            
            if not data['apiresult']['data']['results']:
                continue  
                
            if not data['apiresult']['data']['results'][0]:
                continue
                
            if 'description' not in data['apiresult']['data']['results'][0]:
                continue
            
            
            if data['apiresult']['data']['results'][0]['description']:
                
                descparts=re.findall('\w+',data['apiresult']['data']['results'][0]['description'] )
                descparts.extend(getbigram(descparts))
                descchar=[s for s in descparts if s in database]
            
            else:
                descchar=[]
                
            if data['apiresult']['data']['results'][0]['characters']['available']>0:

                apichar=map(lambda item:item['name'], data['apiresult']['data']['results'][0]['characters']['items'])
                unichar=[]
                [unichar.extend(char.split(" "))for char in apichar]
                bichar=getbigram(unichar)
                unichar.extend(bichar)
                datachar=[s for s in unichar if s in database]
            else: 
                datachar=[]
                
            if data['apiresult']['data']['results'][0]['title']:
                booktitle=data['apiresult']['data']['results'][0]['title']
                unipart=booktitle.split(" ")
                bipart=getbigram(unipart)
                unipart.extend(bipart)
                titlechar=[s for s in unipart if s in database]
            else:
                titlechar
                
            descchar.extend(datachar)
            descchar.extend(titlechar)

            characterlist=list(set(descchar))
            data['charlist']=characterlist
            
            rolelist=charinfo["Role"].values
            roles=[rolelist[np.where(database=="Wolverine")[0].tolist()[0]] if s in database else "unknown" for s in characterlist]
            data['roles']=roles
            
            if len(characterlist)!=len(roles): 
                print "roles retrieved incorrectly" 

        except: 
            print "Exception at %sth entry" %counter
            traceback.print_exc(file=sys.stdout)
            break

        finally:
            counter+=1
    
    return records
    


# In[133]:

print data6[2]['apiresult']['data']['results'][0]['title']
test1=getChar(data6[2:4], database, marveltable)
print test1[0]


# In[132]:

apidata=deepcopy(data1)
apidata.extend(data2)
apidata.extend(data3)
apidata.extend(data4)
apidata.extend(data5)
apidata.extend(data6)
apidata.extend(data7)

print len(apidata)


# In[ ]:




# In[134]:

extracteddata=getChar(apidata, database, marveltable)
print len(extracteddata)


# In[135]:

if extracteddata[0]['apiresult']['data']['results'][0]['id']:
    print "Character Extraction Successful"
else:
    print "Character Extraction Failed, please check input data"


# In[136]:

def getFinaldata(extracteddata):
    finaldata=[]
    for data in extracteddata:
        counter=0
        try:
            if 'charlist' in data and 'roles' in data:
                for character,role in zip(data['charlist'], data['roles']):
                    bookid=data['apiresult']['data']['results'][0]['id'] 
                    booktitle=data['apiresult']['data']['results'][0]['title']
                    finaldata.append([character, role, data['orders'], bookid, booktitle])
        except: 
            print "Exception at %sth entry" %counter
            traceback.print_exc(file=sys.stdout)
            break
            
        finally:
            counter+=1

    return finaldata


# In[137]:

#print len(extracteddata)
finaldata=getFinaldata(extracteddata)
print finaldata[0]



# In[138]:

outfile  = open('marvelherosall.csv', "wb")
writer = csv.writer(outfile, delimiter=',',quotechar='"', quoting=csv.QUOTE_ALL )

for row in finaldata:
    writer.writerow(row)

outfile.close()


# In[143]:

##### export edges
def makeEdges(data):
    edges=[]
    for key, group in groupby(data, lambda x:x[3]):
        chars=map(lambda line: line[0], group)
        
        for combo in combinations(chars, 2):
            #print combo
            edges.append([combo[0], combo[1], key])
    
    return edges
            

edgefile=makeEdges(finaldata)


# In[ ]:




# In[144]:

#### export edge file
print len(edgefile)
outfile  = open('marveledges.csv', "wb")
writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)



for row in edgefile:
    writer.writerow(row)
outfile.close()


# In[ ]:



