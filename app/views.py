from flask import *
import urllib
from app import app
import math
import HTMLParser
import datetime
from lib.reddit import Reddit
from elasticsearch import Elasticsearch,client,helpers

def search_author_reddit(author):
    body = {
        "query": {
            "bool": {
                "must": [
                    {"match": {
                        "author": author
                    }
                    }
                ]
            }
        },
        "highlight": {
            "fields": {
                "text": {}
            }
        }
    }
    ret = es.search(index='my_index', doc_type="my_reddit", body=body)
    return ret['hits']['hits']

def get_reply_children(id):
    body = {
        "query": {
            "bool": {
                "must": [
                    {"match": {
                        "parent":id
                        }
                    }
                ]
            }
        }
    }
    ret=es.search(index='my_index1',doc_type="my_replies", body=body)
    r=[]
    for n in ret['hits']['hits']:
        r.append(n['_source']['id'])
    return r

def search_author_replies(author):
    body = {
        "query": {
            "bool": {
                "must": [
                    {"match": {
                        "author": author
                    }
                    }
                ]
            }
        },
        "highlight": {
            "fields": {
                "text": {}
            }
        }
    }
    ret = es.search(index='my_index1', doc_type="my_replies", body=body)
    return ret['hits']['hits']

def get_reply(id):
    body = {
        "query": {
            "bool": {
                "must": [
                    {"match": {
                        "id":id
                        }
                    }
                ]
            }
        }
    }
    ret=es.search(index='my_index1',doc_type="my_replies", body=body)
    return ret['hits']['hits'][0]

def search_parent(id):
    body = {
        "query": {
            "bool": {
                "must": [
                    {"match": {
                        "id":id
                        }
                    }
                ]
            }
        }
    }
    ret=es.search(index='my_index1',doc_type="my_replies", body=body)
    return ret['hits']['hits'][0]['_source']['parent']

def get_reddit(id):
    body = {
        "query": {
            "bool": {
                "must": [
                    {"match": {
                        "id":id
                        }
                    }
                ]
            }
        }
    }
    ret=es.search(index='my_index',doc_type="my_reddit", body=body)
    return ret['hits']['hits'][0]

def text_search_replies(query):
    body= {
        "query": {
            "bool": {
              "must": [
                { "multi_match": {
                        "query":  query,
                        "fields":     [ "body", "title","selftext_html" ],
                        "operator": "and",
                        "zero_terms_query": "none"
                    }
                },
              ]

            }

        }
    }
    res = es.search(index='my_index1',doc_type="my_replies", body=body)
    hits=res['hits']['hits']
    for hit in hits:
        depth=hit['_source']['depth']
        print hit['_score']
        hit['_score']/=(depth+1)
        print hit['_score']
        path=[]
        id=hit['_source']['id']
        path.insert(0,id)
        print 'hit:\n'
        while depth>=0:
            parent=search_parent(id)
            path.insert(0,parent)
            id=parent
            depth=depth-1
        print path
        hit['path']=path
        print '\n\n'
    return hits


def text_search_reddit(query):
    body = {
        "query": {
            "bool": {
                "must": [
                    {"multi_match": {
                        "query": query,
                        "fields": ["body", "title", "selftext_html"],
                        "operator": "and",
                        "zero_terms_query": "none"
                    }
                    },
                ]

            }

        }
    }
    res = es.search(index='my_index', doc_type="my_reddit", body=body)
    hits = res['hits']['hits']
    return hits

es = Elasticsearch()
with open('app/lib/data.txt') as data_file:
    doc=json.load(data_file)


@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route("/", methods=['GET'])
@app.route("/index", methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/reddit/<id>', methods=['GET'])
def reddit(id):
    """
    :param posting: posting of a article
    :return: the content of this article
    """
    para = str(id)
    hit = get_reddit(id)
    source = hit['_source']
    reddit = Reddit(source['id'], source['title'], HTMLParser.HTMLParser().unescape(source['selftext_html']), datetime.datetime.fromtimestamp(int(source['time'])).strftime('%Y-%m-%d %H:%M:%S'), source['author'], 0 , -1)
    replies = get_reply_children(source['id'])
    children = []
    for id in replies:
        source = get_reply(id)['_source']
        new_reply = Reddit(source['id'], '', source['body'], datetime.datetime.fromtimestamp(int(source['time'])).strftime('%Y-%m-%d %H:%M:%S'), source['author'], 0,0)
        children.append(new_reply)

    if request.args.get('page'):
        page = int(request.args.get('page'))
    else:
        page = 0

    print len(children)

    if request.args.get('ajax') == "1":
        return render_template('ajax_reddit.html', reddits=children[(page * 5):(page * 5) + 5])
    else:
        return render_template('reddits.html', id=para, reddit=reddit, reddits=children[0:5], page=1,total=math.ceil(len(children) / 5))

@app.route('/reply/<id>')
def reply(id):
    """
    :param posting: posting of a article
    :return: the content of this article
    """
    source=get_reply(id)
    title=get_reddit(source['path'][0])['_source']['title']
    source=source['_source']
    reddit = Reddit(source['id'], title, HTMLParser.HTMLParser().unescape(reply['body']), datetime.datetime.fromtimestamp(int(source['time'])).strftime('%Y-%m-%d %H:%M:%S'), source['author'], source['parent'],source['depth'])
    replies= get_reply_children(id)
    children=[]
    for id in replies:
        source=get_reply(id)['_source']
        new_reply=Reddit(source['id'], '', HTMLParser.HTMLParser().unescape(reply['body']), datetime.datetime.fromtimestamp(int(source['time'])).strftime('%Y-%m-%d %H:%M:%S'), source['author'], 0,source['depth'])
        children.append(new_reply)

    if request.args.get('page'):
        page = int(request.args.get('page'))
    else:
        page = 0

    if request.args.get('ajax') == "1":
        return render_template('ajax_reddit.html', reddits=children[(page * 10):(page * 10) + 10])
    else:
        return render_template('reddits.html', id=id, reddit=reddit, reddits=children[0:10], page=1,total=math.ceil(len(children) / 10))


@app.route('/search', methods=['GET'])
def search():
    query = str(request.args.get('query')).strip()
    page = int(request.args.get('page'))
    sort=int(request.args.get('sort'))
    print sort
    print 1234
    hits_reddit=text_search_reddit(query)
    hits_replies=text_search_replies(query)
    if sort==1:
        hits_reddit.sort(key=lambda x:x['_source']['time'],reverse=True)
        hits_replies.sort(key=lambda x: x['_source']['time'], reverse=True)
    elif sort==2:
        hits_reddit.sort(key=lambda x: x['_source']['time'], reverse=True)
        hits_replies.sort(key=lambda x: x['_source']['time'], reverse=True)
    reddits = []
    for hit in hits_reddit:
        source=hit['_source']
        new_reddit=Reddit(source['id'],source['title'],HTMLParser.HTMLParser().unescape(source['selftext_html']),datetime.datetime.fromtimestamp(int(source['time'])).strftime('%Y-%m-%d %H:%M:%S'),source['author'],0,-1)
        reddits.append(new_reddit)
    for hit in hits_replies:
        reply=hit['_source']
        red_id=hit['path'][0]
        source=get_reddit(red_id)
        source=source['_source']

        new_reddit=Reddit(source['id'],source['title'],HTMLParser.HTMLParser().unescape(reply['body']),
                          datetime.datetime.fromtimestamp(int(source['time'])).strftime('%Y-%m-%d %H:%M:%S'),
                          source['author'],reply['id'],reply['depth'])
        reddits.append(new_reddit)

    if request.args.get('ajax') == "1":
        # print (page % (int(math.ceil(len(reddits) / 10))) * 10)
        # print (page % (int(math.ceil(len(reddits) / 10))) * 10) + 10
        return render_template('ajax_grid.html', reddits=reddits[(page % (int(math.ceil(len(reddits) / 10))) * 10):(page % (int(math.ceil(len(reddits) / 10))) * 10) + 10])
    else:
        return render_template('search.html', reddits=reddits[0:10], page= 1, query=query,total=math.ceil(len(reddits) / 10), sort=sort)

@app.route('/author/<id>', methods=['GET'])
def author(id):
    if request.args.get('page'):
        page = int(request.args.get('page'))
    else:
        page = 0
    reddits = []
    reddits_hits=search_author_reddit(id)
    reddits_hits.sort(key=lambda x:x['_source']['time'],reverse=True)
    replies_hits=search_author_replies(id)
    replies_hits.sort(key=lambda x:x['_source']['time'],reverse=True)
    for hit in reddits_hits:
        source=hit['_source']
        new_reddit=Reddit(source['id'],source['title'],HTMLParser.HTMLParser().unescape(reply['body']),datetime.datetime.fromtimestamp(int(source['time'])).strftime('%Y-%m-%d %H:%M:%S'),source['author'],reply['id'])
        reddits.append(new_reddit)
    for hit in replies_hits:
        title=get_reddit(hit['path'])['_source']['title']
        source = hit['_source']
        new_reddit = Reddit(source['id'], title, HTMLParser.HTMLParser().unescape(reply['body']),
                            datetime.datetime.fromtimestamp(int(source['time'])).strftime('%Y-%m-%d %H:%M:%S'),
                            source['author'], reply['id'])
        reddits.append(new_reddit)

    if request.args.get('ajax') == "1":
        return render_template('ajax_reddit.html', reddits=reddits[(page * 10):(page * 10) + 10])
    else:
        return render_template('author.html', reddits=reddits[0:10], page = 1 , id = id, total=math.ceil(len(reddits) / 10))
