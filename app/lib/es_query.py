from elasticsearch import Elasticsearch,client,helpers

import requests
import json
import re

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
    return ret['hits']['hits'][0]['_source']['parent']

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
    return ret['hits']['hits'][0]['_source']['parent']



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

search_body= {
    "query": {
        "bool": {
          "must": [
            { "multi_match": {
                    "query":  "Themes",
                    "fields":     [ "body", "title","selftext_html" ],
                    "operator": "and",
                    "zero_terms_query": "none"
                }
            },
          ]

        }

    }
}


es = Elasticsearch()
with open('data.txt') as data_file:
    doc=json.load(data_file)
res = es.search(index='my_index1',doc_type="my_replies", body=search_body)
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



