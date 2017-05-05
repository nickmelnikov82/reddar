from flask import *
import urllib
from app import app
from lib.thread import Thread

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
    threads = []
    for i in range(100):
        if i % 2 == 0:
            thread = Thread(i, str(i) + "This is a thread title XYXYXYX!","This is the abstract This is a threadThis is a threadThis is a thread", "2016-7-8","whatfuckthisis", "30")
        else:
            thread = Thread(i, str(i) + "This is a thread title XYXYXYX!","This is the abstract This is a threadThis is a threadThis is a threadThis is the abstract  a threadThis is the abstr a threadThis is the abstract  a threadThis is the abstract  a threadThis is the abstract act  a threadThis is the abstract  a threadThis is the abstract This is a threadThis is a threadThis is a threadThis is the abstract This is a threadThis is a threadThis is a thread", "2016-7-8","whatfuckthisis", "30")

        threads.append(thread)
    return render_template('index.html', threads = threads[0:10], page = 2,total = len(threads)/10)


@app.route('/thread/<Id>')
def checkdetail(Id):
    """
    :param posting: posting of a article
    :return: the content of this article
    """
    thread = Thread(Id,str(Id) + "This is a thread title XYXYXYX!", "This is the abstract This is a threadThis is a threadThis is a thread","2016-7-8","whatfuckthisis","30")
    comments = []
    for i in range(500):
        comments.append(i + "this is comments")
    thread.setComment(comments)
    return render_template('thread.html',thread = thread)

@app.route('/search', methods=['GET'])
def search():
    query = str(request.args.get('query')).strip()
    page = int(request.args.get('page'))

    threads = []
    for i in range(100):
        if i % 2 == 0:
            thread = Thread(i, str(i) + "This is a thread title XYXYXYX!","This is the abstract This is a threadThis is a threadThis is a thread", "2016-7-8","whatfuckthisis", "30")
        else:
            thread = Thread(i, str(i) + "This is a thread title XYXYXYX!","This is the abstract This is a threadThis is a threadThis is a threadThis is the abstract  a threadThis is the abstr a threadThis is the abstract  a threadThis is the abstract  a threadThis is the abstract act  a threadThis is the abstract  a threadThis is the abstract This is a threadThis is a threadThis is a threadThis is the abstract This is a threadThis is a threadThis is a thread", "2016-7-8","whatfuckthisis", "30")

        threads.append(thread)


    if page == 1:
        return render_template('index.html', threads=threads[0:10], page=2, query=query, total = len(threads)/10)
    else:
        return render_template('ajax.html', threads=threads[page * 10:page * 10 + 10])
        # return "123"
        # render_template('ajax.html', threads=threads[page * 20:page * 20 + 20])



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