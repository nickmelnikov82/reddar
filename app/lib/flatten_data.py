import json
from types import *
import copy

def fla(js):
    if type(js) is StringType:
        return
    for re in js:
        r=copy.deepcopy(re)
        try:
            r.pop('replies',None)
        except:
            continue
        print r
        rep.append(r)
        try:
            fla(re['replies'])
        except:
            print re
    return





with open('data.txt') as data_file:
    data=json.load(data_file)

count=1
replies={}
output={}
rep=[]
for k,v in data.iteritems():
    red={}
    rep=[]
    red=copy.deepcopy(v)
    fla(v['replies'])
    red['replies']=rep
    output[k]=red
for k,v in output.iteritems():
    reply=v['replies']
    for r in reply:
        replies[count]=r
        count=count+1


with open('data_flattened.txt','w') as outfile:
    json.dump(output,outfile,sort_keys=True);

with open('replies.txt','w') as outfile:
    json.dump(replies,outfile,sort_keys=True);