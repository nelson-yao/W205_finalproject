
# coding: utf-8

# In[1]:

import numpy as np
import json
import re
import sys, traceback
import csv
from itertools import groupby, combinations
from copy import deepcopy
import pandas as pd
from sys import argv

if len(argv)!=2:
    print "Wrong number of arguments"

inputfile=str(argv[1])
# In[2]:

characterdata=pd.read_csv('CharList.txt', header=None, delimiter="\t", names=['Character', "Role", "Origin"])
characterdata.head()

with open(inputfile, "r") as jsonfile:
    data0=json.load(jsonfile)
print "%s records read from file " %len(data0)

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



marveltable=marveltable.append(newdata, ignore_index=True)
database=marveltable['Character'].values

def find_ngrams(input_list, n=2):
    wordtuples=zip(*[input_list[i:] for i in range(n)])
    bigram=[" ".join(s) for s in wordtuples]
    return bigram




trial=data0[12]
if trial['apiresult']['data']['results']:
    print "Trial run is good"
else:
    print "Trial run was nada"


#print set([s for s in bookcharacter if s in database])


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
            roles=[rolelist[np.where(database==s)[0].tolist()[0]] if s in database else "unknown" for s in characterlist]
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



# In[132]:

apidata=deepcopy(data0)
# In[134]:

extracteddata=getChar(apidata, database, marveltable)



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

print "%s characters extracted from API result and comic descriptions" %len(finaldata)



# In[138]:

outfile  = open('marvelchar_test.csv', "wb")
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
print "%s edges retrieved" %len(edgefile)
outfile  = open('marveledges_test.csv', "wb")
writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)


for row in edgefile:
    writer.writerow(row)
outfile.close()


# In[ ]:
