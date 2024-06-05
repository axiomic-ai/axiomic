

class StringList:
    def __init__(self, strings=[]):
        self.strings = strings

    def extend(self, strings):
        self.strings.extend(strings)
    
    def append(self, string):
        self.strings.append(string)