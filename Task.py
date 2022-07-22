# noinspection PyTypeChecker
from datetime import datetime


class Task(object):
    def __init__(self, id, title, list, createdDate, board, members = [], dueDate = datetime(1, 1, 1, 0, 0), removed = False):
        self.title = title
        self.list = list
        self.createdDate = createdDate
        self.members = members
        self.dueDate = dueDate
        self.id = id
        self.board = board
        self.removed = removed

    def from_snapshot(self, snapshot):
        dict = snapshot.to_dict()
        self.id = snapshot.id
        self.title = dict['Title']
        self.list = dict['List']
        self.dueDate = dict['dueDate']
        self.createdDate = dict['createdDate']
        self.board = dict['Board']
        self.members = dict['Members']
        self.removed = dict['Removed']

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
                Id={self.id},\
                Title={self.title}, \
                List={self.list}, \
                createdDate={self.createdDate}, \
                Members={self.members}, \
                Board={self.board},\
                dueDate={self.dueDate}\
            )'
        )
