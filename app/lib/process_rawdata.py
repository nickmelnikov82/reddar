import json
from types import *
import copy

def sub(js):
    # thin the original data, remove useless data
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
    return res;


def fla(js):
    # flatten the replies part using recursion, discard those abnormal replies
    if type(js) is StringType:
        return
    for re in js:
        if type(re) is not DictType:
            continue
        for k,v in re.iteritems():
            r=copy.deepcopy(v)
            try:
                r.pop('replies',None)
            except:
                continue
            rep.append(r)
            try:
                fla(re['replies'])
            except:
                print re
    return


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





#flatten replies
data=output
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