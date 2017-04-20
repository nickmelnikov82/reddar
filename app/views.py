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
    for i in range(10):
        thread = Thread(i,str(i) + "This is a thread title XYXYXYX!", "This is the abstract This is a threadThis is a threadThis is a thread","2016-7-8","whatfuckthisis","30")
        threads.append(thread)
    return render_template('index.html', threads = threads)


@app.route('/thread/<Id>')
def showdetail(Id):
    """
    :param posting: posting of a article
    :return: the content of this article
    """
    thread = Thread(Id,str(Id) + "This is a thread title XYXYXYX!", "This is the abstract This is a threadThis is a threadThis is a thread","2016-7-8","whatfuckthisis","30")
    return render_template('thread.html',thread = thread)
    