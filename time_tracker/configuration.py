from collections import namedtuple

class Configuration(object):
    def __init__(self, filename):
        self.filename = filename

    def addTask(self, taskname, tasktps):
        pass