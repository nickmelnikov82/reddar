class Thread:
    def __init__(self, Id, title, abstract, time, author, comment_number):
    	self.Id = Id;
        self.title = title
        self.abstract = abstract
        self.time = time
        self.author = author
        self.comment_number = comment_number

    def setComment(self, comments):
        self.comments = []
        for comment in comments:
            self.comments.append(comment)

