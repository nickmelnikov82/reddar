from flask import *
import urllib
from app import app
from lib.thread import Thread
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


@app.route('/reddit/<id>')
def check_thread_detail(id):
    """
    :param posting: posting of a article
    :return: the content of this article
    """
    hit = get_reddit(id)
    source = hit['_source']
    reddit = Reddit(source['id'], source['title'], source['selftext_html'], source['time'], source['author'], 0)
    replies = get_reply_children(source['id'])
    children = []
    for id in replies:
        source = get_reply(id)['_source']
        new_reply = Reddit(source['id'], '', source['body'], source['time'], source['author'], 0)
        print source['body']
        children.append(new_reply)
    # for i in range(100):
    #     if i % 2 == 0:
    #         thread = Thread(i, str(i) + "This is a thread title XYXYXYX!","This is the abstract This is a threadThis is a threadThis is a thread", "2016-7-8","whatfuckthisis", "30")
    #     else:
    #         thread = Thread(i, str(i) + "This is a thread title XYXYXYX!","This is the abstract This is a threadThis is a threadThis is a threadThis is the abstract  a threadThis is the abstr a threadThis is the abstract  a threadThis is the abstract  a threadThis is the abstract act  a threadThis is the abstract  a threadThis is the abstract This is a threadThis is a threadThis is a threadThis is the abstract This is a threadThis is a threadThis is a thread", "2016-7-8","whatfuckthisis", "30")

    return render_template('thread.html', thread=reddit, comments=children)

@app.route('/comment/<Id>')
def check_comment_detail(Id):
    """
    :param posting: posting of a article
    :return: the content of this article
    """
    hit=get_reddit(id)
    parent_id=search_parent(id)
    source=get_reply(parent_id)['_source']
    reddit = Reddit(source['id'], '', source['body'], source['time'], source['author'], 0)
    replies=get_reply_children(parent_id)
    children=[]
    for id in replies:
        source=get_reply(['_source'])
        new_reply=Reddit(source['id'], '', source['body'], source['time'], source['author'], 0)
        children.append(new_reply)
    # for i in range(100):
    #     if i % 2 == 0:
    #         thread = Thread(i, str(i) + "This is a thread title XYXYXYX!","This is the abstract This is a threadThis is a threadThis is a thread", "2016-7-8","whatfuckthisis", "30")
    #     else:
    #         thread = Thread(i, str(i) + "This is a thread title XYXYXYX!","This is the abstract This is a threadThis is a threadThis is a threadThis is the abstract  a threadThis is the abstr a threadThis is the abstract  a threadThis is the abstract  a threadThis is the abstract act  a threadThis is the abstract  a threadThis is the abstract This is a threadThis is a threadThis is a threadThis is the abstract This is a threadThis is a threadThis is a thread", "2016-7-8","whatfuckthisis", "30")

    return render_template('thread.html',thread = reddit, comments = children)


@app.route('/search', methods=['GET'])
def search():
    query = str(request.args.get('query')).strip()
    page = int(request.args.get('page'))
    sort=int(request.args.get('sort'))
    hits_reddit=text_search_reddit(query)
    hits_replies=text_search_replies(query)
    if sort==1:
        hits_reddit.sort(key=lambda x:x._source.time,reversed=True)
        hits_replies.sort(key=lambda x: x._source.time, reversed=True)
    elif sort==2:
        hits_reddit.sort(key=lambda x: x._source.score, reversed=True)
        hits_replies.sort(key=lambda x: x._source.score, reversed=True)
    reddits = []
    for hit in hits_reddit:
        source=hit['_source']
        new_reddit=Reddit(source['id'],source['title'],source['selftext_html'],source['time'],source['author'],0)
        reddits.append(new_reddit)
    for hit in hits_replies:
        reply=hit['_source']
        red_id=hit['path'][0]
        source=get_reddit(red_id)
        source=source['_source']
        new_reddit=Reddit(source['id'],source['title'],reply['body'],source['time'],source['author'],reply['id'])
        reddits.append(new_reddit)

    # for i in range(100):
    #     if i % 2 == 0:
    #         thread = Thread(i, str(i) + "This is a thread title XYXYXYX!","This is the abstract This is a threadThis is a threadThis is a thread", "2016-7-8","whatfuckthisis", "30")
    #     else:
    #         thread = Thread(i, str(i) + "This is a thread title XYXYXYX!","This is the abstract This is a threadThis is a threadThis is a threadThis is the abstract  a threadThis is the abstr a threadThis is the abstract  a threadThis is the abstract  a threadThis is the abstract act  a threadThis is the abstract  a threadThis is the abstract This is a threadThis is a threadThis is a threadThis is the abstract This is a threadThis is a threadThis is a thread", "2016-7-8","whatfuckthisis", "30")



    if page == 0:
        return render_template('search.html', reddits=reddits[0:10], page=2, query=query, total = len(reddits)/10)
    else:
        return render_template('ajax.html', reddits=reddits[page * 10:page * 10 + 10])

#
# }
#
#
#
# def index(){
# top 100 thread sort by time
# }
#
# def search(query, sort = time){
#
# NLP process
# search thread by query term
# }
#
# def checkdetail(id){
# get all comment with id as parent id
# }
#
# def goback(id){
#
# get parent id
#
# checkdetail(parent id)
#
# }
#
# def searchauthor(author name){
#
# get thread by query =  name and sort by time
#
# }