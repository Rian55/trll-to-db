# noinspection PyTypeChecker
from datetime import datetime


class Task(object):
    def __init__(self, id, title, list, createdDate, board, members = [], dueDate = datetime(1, 1, 1, 0, 0)):
        self.title = title
        self.list = list
        self.createdDate = createdDate
        self.members = members
        self.dueDate = dueDate
        self.id = id
        self.board = board

    def from_dict(self, snapshot):
        dict = u'{}'.format(snapshot.to_dict())
        self.id = snapshot.id
        self.title = dict['Title']
        self.list = dict['List']
        self.dueDate = dict['dueDate']
        self.createdDate = dict['createdDate']
        self.board = dict['Board']
        self.members = dict['Members']

    def to_dict(self):
        query = {
            u'Title': self.title,
            u'List': self.list,
            u'Members': self.members,
            u'dueDate': self.dueDate,
            u'createdDate': self.createdDate,
            u'Board': self.board,
            u'Removed': False,
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
