class Reddit:
    def __init__(self, id, title, body, time, author,reply_id,depth):
        self.id = id;
        self.title = title
        self.body = body
        self.time = time
        self.author = author
        self.reply_id=reply_id
        self.depth=depth

    def setComment(self, comments):
        self.comments = []
        for comment in comments:
            self.comments.append(comment)