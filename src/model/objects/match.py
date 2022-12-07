

class Match:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __key(self):
        return self.start, self.end

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__key() == other.__key()

    def __hash__(self):
        return hash(self.__key())

    def __getitem__(self, item):
        return self.__dict__[item]
