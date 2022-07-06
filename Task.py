class Task(object):
    def __init__(self, id, title, list, createdDate, board, members = [], dueDate = None):
        self.title = title
        self.list = list
        self.createdDate = createdDate
        self.members = members
        self.dueDate = dueDate
        self.id = id
        self.board = board

    def to_dict(self):
        query = {
            u'Title': self.title,
            u'List': self.list,
            u'Members': self.members,
            u'dueDate': self.dueDate,
            u'createdDate': self.createdDate,
            u'Board': self.board,
        }
        return query

    def __repr__(self):
        return(
            f'tasks(\
                Title={self.title}, \
                List={self.list}, \
                createdDate={self.createdDate}, \
                Members={self.members}, \
                Board={self.board},\
                dueDate={self.dueDate}\
            )'
        )
