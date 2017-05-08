import urllib2
import json

hdr = {'User-Agent': 'osx:r/relationships.single.result:v1.0 (by /u/<info_retrieval>)'}
url = 'https://www.reddit.com/r/IAmA/.json?sort=hot&t=all&limit=200'
req = urllib2.Request(url, headers=hdr)
text_data = urllib2.urlopen(req).read()
data = json.loads(text_data)
output={};
i=1;
print len(data['data']['children'])

for k in data['data']['children']:

    link=k['data']['url']+'.json'
    req = urllib2.Request(link, headers=hdr)
    text = urllib2.urlopen(req).read()
    try:
        output[i]=json.loads(text)
    except:
        print text
    i=i+1

print i

with open('rawdata.txt','w') as outfile:
    json.dump(output,outfile,sort_keys=True);