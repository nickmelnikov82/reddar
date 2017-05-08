from elasticsearch import Elasticsearch,client,helpers

import requests
import json
import re

es = Elasticsearch()  # use default of localhost, port 9200
json_file=open('data_flattened.txt')                                  #load coupus file
js_data = json.load(json_file)
replies_file=open('replies.txt')
replies=json.load(replies_file)


# setting es body for further creating
create_body= {
    "settings": {
        "analysis": {
            "analyzer": {
                "my_stop": {
                    "type":      "custom",
                    "tokenizer": "standard",
                    "filter": [
                            "lowercase",
                            "porter_stem",
                            "english_stop"
                            ],
                }
            },
            "filter": {
                "english_stop":{
                               "type":"stop",
                               "stopwords":"_english_"
                }
            }
        },
    },
    "mappings":{
        "my_reddit":{
            "properties":{
                "author":{
                    "type":"text",
                },
                "score":{
                    "type":"integer",
                },
                "title":{
                    "type":"string",
                    "analyzer": "my_stop",
                },
                "selftext_html":{
                    "type":"string",
                    "analyzer": "my_stop" ,
                },
                "time":{
                    "type":"long",
                },
                "ups":{
                    "type":"integer",
                },
                "id":{
                    "type":"string"
                },
                "replies":{
                    "type":"nested",
                    "properties":{
                        "author":{
                            "type":"string"
                        },
                        "body":{
                            "type":"string",
                            "analyzer":"my_stop"
                        },
                        "id":{
                            "type":"string"
                        },
                        "parent":{
                            "type":"string"
                        },
                        "depth":{
                            "type":"integer"
                        },
                        "time":{
                            "type":"long"
                        },
                        "score":{
                            "type":"integer"
                        },
                        "ups":{
                            "type":"integer"
                        }
                    }
                }
            }
        }

    }
}

es.indices.delete(index="my_index")
es.indices.create(index='my_index',body=create_body)
actions=[
    {
        "_index": "my_index",
        "_type": "my_reddit",
        "_id": k,
        "_source": {
            "author": v['author'],
            "replies": v['replies'],
            "title": v['title'],
            "score": v['score'],
            "time": v['time'],
            "selftext_html": v['selftext_html'],
            "ups":v["ups"],
            "id":v['id']
        }
    }
    for k, v in js_data.iteritems()
]
helpers.bulk(es, actions)

#the create body of replies
create_body2= {
    "settings": {
        "analysis": {
            "analyzer": {
                "my_stop": {
                    "type":      "custom",
                    "tokenizer": "standard",
                    "filter": [
                            "lowercase",
                            "porter_stem",
                            "english_stop"
                            ],
                }
            },
            "filter": {
                "english_stop":{
                               "type":"stop",
                               "stopwords":"_english_"
                }
            }
        },
    },
    "mappings":{
        "my_replies":{
            "properties":{
                "author":{
                    "type":"string"
                },
                "body":{
                    "type":"string",
                    "analyzer":"my_stop"
                },
                "id":{
                    "type":"string"
                },
                "parent":{
                    "type":"string"
                },
                "depth":{
                    "type":"integer"
                },
                "time":{
                    "type":"long"
                },
                "score":{
                    "type":"integer"
                },
                "ups":{
                    "type":"integer"
                }
            }
        }
    }
}
es.indices.delete(index='my_index1')
es.indices.create(index='my_index1',body=create_body2)
actions=[
    {
        "_index": "my_index1",
        "_type": "my_replies",
        "_id": k,
        "_source": {
            "author": v['author'],
            "depth": v['depth'],
            "parent": v['parent'],
            "score": v['score'],
            "time": v['time'],
            "body":v['body'],
            "ups":v['ups'],
            "id":v['id']
        }
    }
    for k, v in replies.iteritems()
]
helpers.bulk(es, actions)