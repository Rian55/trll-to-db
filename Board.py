class Board(object):
    def __init__(self, id, name, members = [], lists = []):
        self.name = name
        self.members = members
        self.lists = lists
        self.id = id

    def to_dict(self):
        query = {
            u'Name': self.name,
            u'Members': self.members,
            u'Lists': self.lists,
        }
        return query

    def __repr__(self):
        return(
            f'boards(\
                Name={self.name}, \
                Members={self.members}, \
                Lists={self.lists} \
            )'
        )
