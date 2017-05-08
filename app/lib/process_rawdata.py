import json
from types import *

def sub(js):
    res={}
    js=js['data']
    res['author'] = js.get('author','')
    if res['author']=='':
        return
    res['depth'] = js.get('depth','')
    res['body'] = js.get('body','')
    res['score'] = js.get('score','')
    res['ups'] = js.get('ups','')
    res['time'] = js.get('created_utc','')
    res['id']=js.get('id','');
    parent=js.get('parent_id','')
    try:
        parent=parent.split('_')[1]
    except:
        print parent
    res['parent']=parent
    rep=js.get('replies','')
    try:
        rep=rep['data']['children']
    except:
        return res;
    if type(rep) is ListType:
        res['replies']=[]
        for r in rep:
            res['replies'].append(sub(r))
    elif type(rep) is DictType:
        res['replies']=sub(rep);
    m={}
    m[res['id']]=res
    return m;





with open('rawdata.txt') as data_file:
    data=json.load(data_file)

output={}
for k,v in data.iteritems():
    red={}
    data=v[0]['data']['children'][0]['data']
    red['score']=data['score']
    red['id']=data['id']
    red['author'] = data['author']
    red['ups'] = data['ups']
    red['time'] = data['created_utc']
    red['title'] = data['title']
    red['selftext_html']=data['selftext_html']
    rep = v[1]['data']['children']
    if type(rep) is ListType:
        red['replies'] = []
        for r in rep:
            red['replies'].append(sub(r))
    elif type(rep) is DictType:
        red['replies'] = sub(rep);
    output[k]=red

with open('data.txt','w') as outfile:
    json.dump(output,outfile,sort_keys=True);