from json import JSONEncoder

idGenerate = 0

class Pessoa(object):

    def getId(self):
        global idGenerate
        idGenerate += 1
        return idGenerate

    def __init__(self, nome):
        self.id = self.getId()
        self.nome = nome