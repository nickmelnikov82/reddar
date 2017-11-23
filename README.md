# README

## What is Reddar?
* Reddar is a retrieval system based on elasticsearch for Reddit data. We already fetch part of data from Reddit "IAMA" thread for experiment by Reddit Jason APIs, you may want to retrieve own data to build corpus!

## Why is Reddar(Difference from Reddit)?
* ####Userability 
	* Restructured data and re-designed interaction

* ####Flexibility
	* Improved search functionality with elastic seach and organized search results for different demand

## Feature
 -  can check out near by farmers markets.
 -  can see which vendors have a specific product.
 -  can specific product and want to know which vendor has it and is open now.
 -  can be able to view all local products from all local vendors.
 -  can go to a farmers market page and check which farmers markets are open now.
 -  can explore markets around me and see the vendors at each market and what each vendor has.
 -  can see some popular products nearby
 -  can save products to my grocery list. 
 -  can review Farmers Markets I’ve been to. 
 -  can request system help schedule a reasonable shopping plan base on time and location


## Demo
Here is a live demo deployed on heroku with partial data :  [Reddar](https://github.com/HuimingJia/Reddar)

## Notes
Before start flask application, please make ure you already start local elasticsearch(which is for building index and work as database in our application) first! You can start application by run commands in the terminal as follows. 

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

