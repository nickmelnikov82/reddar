# README

## What is Reddar?
* Reddar is a retrieval system based on elasticsearch and python flask for Reddit data. We already fetch part of data from Reddit "IAMA" thread for experiment, you may want to retrieve own data by Reddit json APIs to build corpus!

## Why Reddar (Difference from Reddit)?
#### Userability 
- Restructured data and re-designed interaction
- ![diagram](https://github.com/HuimingJia/Reddar/blob/master/images/Structure.png)

#### Flexibility
- Improved search functionality with elastic seach and organized search results for different demand

## Feature
 - Full-text search Reddit data with elastic search
 - Order search results by relevance, time, score and distinguish result by theme and replies
 - Flatten reddit content and re-arrange replies by time
 - Check user history
 
## Index and Query
- Article(Theme) index
	- Indexing the article content separately without replies
	- Standard tokenizer, porter stem, english stop
-  Replies index
	- Indexing all the replies content and each their parent. (The replies' which depth is 0 will have article(theme) as parent
	- Standard tokenizer, porter stem, english stop
- Text Search: 
	- Search all relevant articles
	- Search all relevant replies
	- Reconstruct the structure through depth and parent fields
	
- Author Search: 
	- Search all articles posted by the author
	- Search all replies posted by the author
- Weighting
	- we considered the replies’ relevance decrease as they go deeper, which means the replies close to the root (the reddit article ) are more relevant to those far from the root. Assign the first level of replies as depth 0. The weight of a reply is 1/(1+depth).
- Sorting
 	- We support 3 kinds of sorting: relevance, time, score (upvotes- downvotes)


## Demo
Here is a live demo deployed on heroku with partial data :  [Reddar](https://github.com/HuimingJia/Reddar)

## Notes
Before starting flask application, please make sure you already start local elasticsearch(which is for building index and work as database in our application) first! You can start application by run commands in the terminal as follows. 

```
- <elasticsearch path>/bin/elasticsearch
```
after elasticsearch started

```
- python <Application path>/run.py
```

## Site Snapshot

### Home Page
![Home Page](https://github.com/HuimingJia/Reddar/blob/master/images/HomePage.png)

### Search Bar
![Search Bar](https://github.com/HuimingJia/Reddar/blob/master/images/SearchFunction.png) 

### Search Result
![Search Result](https://github.com/HuimingJia/Reddar/blob/master/images/SearchResult.png)

### Reddit Page
![Reddit Page](https://github.com/HuimingJia/Reddar/blob/master/images/Reddit.png)

### Reply Page
![Reply Page](https://github.com/HuimingJia/Reddar/blob/master/images/Reply.png)

### User History
![User History](https://github.com/HuimingJia/Reddar/blob/master/images/UserReddit.png) 

## Index Schema


## Development
Want to contribute? Great!

To fix a bug or enhance an existing module, follow these steps:

	1.Fork the repo
	2.Create a new branch (`git checkout -b improve-feature`)
	3.Make the appropriate changes in the files
	4.Add changes to reflect the changes made
	5.Commit your changes (`git commit -am 'Improve feature'`)
	6.Push to the branch (`git push origin improve-feature`)
	7.Create a Pull Request

## Built with
>
- [ElasticSearch](https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/index.html) - Elasticsearch is a search engine based on Lucene. It provides a distributed, multitenant-capable full-text search engine with an HTTP web interface and schema-free JSON documents.
- [Masonry](https://masonry.desandro.com/) - Masonry is a JavaScript grid layout library. It works by placing elements in optimal position based on available vertical space, sort of like a mason fitting stones in a wall. You’ve probably seen it in use all over the Internet.
- [Flask](http://flask.pocoo.org/) - Flask is a microframework for Python based on Werkzeug, Jinja 2 and good intentions.
- [Reddit APIs](https://www.reddit.com/dev/api/) - Reddit json APIs
- [Bootstrap](http://getbootstrap.com/) - Build responsive, mobile-first projects on the web with the world's most popular front-end component library.

## To-Do
- Build a richer corpus to test the robustness of our application
- Analyze url direct to media content and directly show media content in application
- Definie Synonyms to explore more interesting search functionalities

## Team

[![Huiming Jia](https://avatars1.githubusercontent.com/u/22848271?s=200)](https://github.com/HuimingJia)  | [![MingyangJin](https://avatars2.githubusercontent.com/u/23490377?s=200)](https://github.com/HuxTim)|
---|---|
[Huiming Jia](https://github.com/HuimingJia) |[MingyangJin](https://github.com/MingyangJin) |

